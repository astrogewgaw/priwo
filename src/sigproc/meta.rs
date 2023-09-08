use nom::{
    branch::alt,
    bytes::streaming::tag,
    combinator::map_res,
    multi::{length_data, length_value, many_till},
    number::streaming::{f64, u32, u8},
    number::Endianness,
    sequence::preceded,
    IResult,
};

use crate::err::PriwoError;

type ParseResult<'a, T> = IResult<&'a [u8], T, PriwoError>;
type FieldResult<'a> = ParseResult<'a, Field<'a>>;

fn hdrstr(s: &'static str, endian: Endianness) -> impl FnMut(&[u8]) -> ParseResult<&[u8]> {
    move |input: &[u8]| length_value(u32(endian), tag(s))(input)
}

fn hdrbeg(input: &[u8], endian: Endianness) -> ParseResult<&[u8]> {
    hdrstr("HEADER_START", endian)(input)
}

fn hdrend(input: &[u8], endian: Endianness) -> ParseResult<&[u8]> {
    hdrstr("HEADER_END", endian)(input)
}

macro_rules! numeric {
    ($header_name:ident, $ty:ident, $param:ident) => {
        fn $header_name(input: &[u8], endian: Endianness) -> FieldResult {
            let (remaining, value) =
                preceded(hdrstr(stringify!($header_name), endian), $ty(endian))(input)?;
            Ok((remaining, Field::$param(value)))
        }
    };
}

macro_rules! boolean {
    ($header_name:ident, $param:ident) => {
        fn $header_name(input: &[u8], endian: Endianness) -> FieldResult {
            let (remaining, value) =
                preceded(hdrstr(stringify!($header_name), endian), u32(endian))(input)?;
            Ok((remaining, Field::$param(value == 1)))
        }
    };
}

macro_rules! string {
    ($header_name:ident, $param:ident) => {
        fn $header_name(input: &[u8], endian: Endianness) -> FieldResult {
            let (remaining, value) = preceded(
                hdrstr(stringify!($header_name), endian),
                map_res(length_data(u32(endian)), std::str::from_utf8),
            )(input)?;
            Ok((remaining, Field::$param(value)))
        }
    };
}

string!(filename, Filename);
numeric!(telescope_id, u32, TelescopeId);
string!(telescope, Telescope);
numeric!(machine_id, u32, MachineId);
numeric!(data_type, u32, DataType);
string!(rawdatafile, Rawdatafile);
string!(source_name, SourceName);
boolean!(barycentric, Barycentric);
boolean!(pulsarcentric, Pulsarcentric);
numeric!(az_start, f64, AzStart);
numeric!(za_start, f64, ZaStart);
numeric!(src_raj, f64, SrcRaj);
numeric!(src_dej, f64, SrcDej);
numeric!(tstart, f64, Tstart);
numeric!(tsamp, f64, Tsamp);
numeric!(nbits, u32, Nbits);
numeric!(nsamples, u32, Nsamples);
numeric!(fch1, f64, Fch1);
numeric!(foff, f64, Foff);
numeric!(fchannel, f64, Fchannel);
numeric!(nchans, u32, Nchans);
numeric!(nifs, u32, Nifs);
numeric!(refdm, f64, Refdm);
numeric!(flux, f64, Flux);
numeric!(period, f64, Period);
numeric!(nbeams, u32, Nbeams);
numeric!(ibeam, u32, Ibeam);
numeric!(hdrlen, u32, Hdrlen);
numeric!(pb, f64, Pb);
numeric!(ecc, f64, Ecc);
numeric!(asini, f64, Asini);
numeric!(orig_hdrlen, u32, OrigHdrlen);
numeric!(new_hdrlen, u32, NewHdrlen);
numeric!(sampsize, u32, Sampsize);
numeric!(bandwidth, f64, Bandwidth);
numeric!(fbottom, f64, Fbottom);
numeric!(ftop, f64, Ftop);
string!(obs_date, ObsDate);
string!(obs_time, ObsTime);
numeric!(accel, f64, Accel);

fn signed(input: &[u8], endian: Endianness) -> FieldResult {
    let (remaining, value) = preceded(hdrstr("signed", endian), u8)(input)?;
    Ok((remaining, Field::Signed(value == 1)))
}

enum Field<'a> {
    Filename(&'a str),
    TelescopeId(u32),
    Telescope(&'a str),
    MachineId(u32),
    DataType(u32),
    Rawdatafile(&'a str),
    SourceName(&'a str),
    Barycentric(bool),
    Pulsarcentric(bool),
    AzStart(f64),
    ZaStart(f64),
    SrcRaj(f64),
    SrcDej(f64),
    Tstart(f64),
    Tsamp(f64),
    Nbits(u32),
    Nsamples(u32),
    Fch1(f64),
    Foff(f64),
    Fchannel(f64),
    Nchans(u32),
    Nifs(u32),
    Refdm(f64),
    Flux(f64),
    Period(f64),
    Nbeams(u32),
    Ibeam(u32),
    Hdrlen(u32),
    Pb(f64),
    Ecc(f64),
    Asini(f64),
    OrigHdrlen(u32),
    NewHdrlen(u32),
    Sampsize(u32),
    Bandwidth(f64),
    Fbottom(f64),
    Ftop(f64),
    ObsDate(&'a str),
    ObsTime(&'a str),
    Signed(bool),
    Accel(f64),
}

#[derive(Debug, Default)]
pub struct SIGPROCMetadata<'a> {
    pub filename: Option<&'a str>,
    pub telescope_id: Option<u32>,
    pub telescope: Option<&'a str>,
    pub machine_id: Option<u32>,
    pub data_type: Option<u32>,
    pub rawdatafile: Option<&'a str>,
    pub source_name: Option<&'a str>,
    pub barycentric: Option<bool>,
    pub pulsarcentric: Option<bool>,
    pub az_start: Option<f64>,
    pub za_start: Option<f64>,
    pub src_raj: Option<f64>,
    pub src_dej: Option<f64>,
    pub tstart: Option<f64>,
    pub tsamp: Option<f64>,
    pub nbits: Option<u32>,
    pub nsamples: Option<u32>,
    pub fch1: Option<f64>,
    pub foff: Option<f64>,
    pub fchannel: Option<f64>,
    pub nchans: Option<u32>,
    pub nifs: Option<u32>,
    pub refdm: Option<f64>,
    pub flux: Option<f64>,
    pub period: Option<f64>,
    pub nbeams: Option<u32>,
    pub ibeam: Option<u32>,
    pub hdrlen: Option<u32>,
    pub pb: Option<f64>,
    pub ecc: Option<f64>,
    pub asini: Option<f64>,
    pub orig_hdrlen: Option<u32>,
    pub new_hdrlen: Option<u32>,
    pub sampsize: Option<u32>,
    pub bandwidth: Option<f64>,
    pub fbottom: Option<f64>,
    pub ftop: Option<f64>,
    pub obs_date: Option<&'a str>,
    pub obs_time: Option<&'a str>,
    pub signed: Option<bool>,
    pub accel: Option<f64>,
    pub endian: Option<Endianness>,
}

fn header<'a>(i: &'a [u8]) -> ParseResult<'a, (Endianness, Vec<Field<'a>>)> {
    let magic_b = hdrbeg(i, Endianness::Big);
    let magic_l = hdrbeg(i, Endianness::Little);
    let (i, endian) = if let Ok((i, _)) = magic_b {
        (i, Endianness::Big)
    } else if let Ok((i, _)) = magic_l {
        (i, Endianness::Little)
    } else {
        return Err(magic_l.err().unwrap());
    };
    let (i, (headers, _)) = many_till(
        alt((
            alt((
                |i: &'a [u8]| telescope_id(i, endian),
                |i: &'a [u8]| machine_id(i, endian),
                |i: &'a [u8]| data_type(i, endian),
                |i: &'a [u8]| nbits(i, endian),
                |i: &'a [u8]| nchans(i, endian),
                |i: &'a [u8]| nifs(i, endian),
                |i: &'a [u8]| nbeams(i, endian),
                |i: &'a [u8]| nsamples(i, endian),
                |i: &'a [u8]| ibeam(i, endian),
                |i: &'a [u8]| hdrlen(i, endian),
                |i: &'a [u8]| orig_hdrlen(i, endian),
                |i: &'a [u8]| new_hdrlen(i, endian),
                |i: &'a [u8]| sampsize(i, endian),
            )),
            alt((
                |i: &'a [u8]| az_start(i, endian),
                |i: &'a [u8]| za_start(i, endian),
                |i: &'a [u8]| src_raj(i, endian),
                |i: &'a [u8]| src_dej(i, endian),
                |i: &'a [u8]| tstart(i, endian),
                |i: &'a [u8]| tsamp(i, endian),
                |i: &'a [u8]| fch1(i, endian),
                |i: &'a [u8]| foff(i, endian),
                |i: &'a [u8]| fchannel(i, endian),
                |i: &'a [u8]| refdm(i, endian),
                |i: &'a [u8]| flux(i, endian),
                |i: &'a [u8]| period(i, endian),
                |i: &'a [u8]| pb(i, endian),
                |i: &'a [u8]| ecc(i, endian),
                |i: &'a [u8]| asini(i, endian),
                |i: &'a [u8]| bandwidth(i, endian),
                |i: &'a [u8]| fbottom(i, endian),
                |i: &'a [u8]| ftop(i, endian),
                |i: &'a [u8]| accel(i, endian),
            )),
            alt((
                |i: &'a [u8]| barycentric(i, endian),
                |i: &'a [u8]| pulsarcentric(i, endian),
                |i: &'a [u8]| signed(i, endian),
            )),
            alt((
                |i: &'a [u8]| filename(i, endian),
                |i: &'a [u8]| telescope(i, endian),
                |i: &'a [u8]| rawdatafile(i, endian),
                |i: &'a [u8]| source_name(i, endian),
                |i: &'a [u8]| obs_date(i, endian),
                |i: &'a [u8]| obs_time(i, endian),
            )),
        )),
        |i: &'a [u8]| hdrend(i, endian),
    )(i)?;
    Ok((i, (endian, headers)))
}

impl<'a> SIGPROCMetadata<'a> {
    pub fn from_bytes(i: &'a [u8]) -> Result<(&'a [u8], Self), PriwoError> {
        let (i, (endian, headers)) = header(i).map_err(|e| match e {
            nom::Err::Incomplete(_) => PriwoError::IncompleteMetadata,
            nom::Err::Error(e) => e,
            nom::Err::Failure(e) => e,
        })?;

        let mut s = Self::default();

        for header in headers {
            match header {
                Field::Filename(x) => s.filename = Some(x),
                Field::TelescopeId(x) => s.telescope_id = Some(x),
                Field::Telescope(x) => s.telescope = Some(x),
                Field::MachineId(x) => s.machine_id = Some(x),
                Field::DataType(x) => s.data_type = Some(x),
                Field::Rawdatafile(x) => s.rawdatafile = Some(x),
                Field::SourceName(x) => s.source_name = Some(x),
                Field::Barycentric(x) => s.barycentric = Some(x),
                Field::Pulsarcentric(x) => s.pulsarcentric = Some(x),
                Field::AzStart(x) => s.az_start = Some(x),
                Field::ZaStart(x) => s.za_start = Some(x),
                Field::SrcRaj(x) => s.src_raj = Some(x),
                Field::SrcDej(x) => s.src_dej = Some(x),
                Field::Tstart(x) => s.tstart = Some(x),
                Field::Tsamp(x) => s.tsamp = Some(x),
                Field::Nbits(x) => s.nbits = Some(x),
                Field::Nsamples(x) => s.nsamples = Some(x),
                Field::Fch1(x) => s.fch1 = Some(x),
                Field::Foff(x) => s.foff = Some(x),
                Field::Fchannel(x) => s.fchannel = Some(x),
                Field::Nchans(x) => s.nchans = Some(x),
                Field::Nifs(x) => s.nifs = Some(x),
                Field::Refdm(x) => s.refdm = Some(x),
                Field::Flux(x) => s.flux = Some(x),
                Field::Period(x) => s.period = Some(x),
                Field::Nbeams(x) => s.nbeams = Some(x),
                Field::Ibeam(x) => s.ibeam = Some(x),
                Field::Hdrlen(x) => s.hdrlen = Some(x),
                Field::Pb(x) => s.pb = Some(x),
                Field::Ecc(x) => s.ecc = Some(x),
                Field::Asini(x) => s.asini = Some(x),
                Field::OrigHdrlen(x) => s.orig_hdrlen = Some(x),
                Field::NewHdrlen(x) => s.new_hdrlen = Some(x),
                Field::Sampsize(x) => s.sampsize = Some(x),
                Field::Bandwidth(x) => s.bandwidth = Some(x),
                Field::Fbottom(x) => s.fbottom = Some(x),
                Field::Ftop(x) => s.ftop = Some(x),
                Field::ObsDate(x) => s.obs_date = Some(x),
                Field::ObsTime(x) => s.obs_time = Some(x),
                Field::Signed(x) => s.signed = Some(x),
                Field::Accel(x) => s.accel = Some(x),
            }
        }

        s.endian = Some(endian);

        if s.nbits.is_none()
            && s.nifs.is_none()
            && s.nchans.is_none()
            && (s.tsamp.is_none() && s.sampsize.is_none())
        {
            return Err(PriwoError::InvalidMetadata);
        }

        if s.data_type.unwrap() == 1
            && (s.fch1.is_none() && s.fbottom.is_none() && s.ftop.is_none())
            && (s.foff.is_none() && s.fchannel.is_none() && s.bandwidth.is_none())
        {
            return Err(PriwoError::InvalidMetadata);
        }

        if s.data_type.unwrap() == 2 && s.nifs.unwrap() != 1 && s.nchans.unwrap() != 1 {
            return Err(PriwoError::InvalidMetadata);
        }

        let nifs = s.nifs.unwrap();
        let nbits = s.nbits.unwrap();
        let nchans = s.nchans.unwrap();
        let nsamp = (i.len() as u32 * 8) / nbits / nchans / nifs;
        s.nsamples = Some(nsamp);

        Ok((i, s))
    }
}

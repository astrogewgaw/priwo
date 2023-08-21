use super::SIGPROCMetadata;
use crate::err::PriwoError;
use ndarray::{Array, Array1, Array2};
use nom::number::Endianness;

fn parse(i: &'_ [u8]) -> Result<(Array2<f64>, Endianness, SIGPROCMetadata<'_>), PriwoError> {
    let (raw, endian, meta) = SIGPROCMetadata::from_bytes(i)?;

    let signed = meta.signed;
    let nbits = meta.nbits.unwrap();
    let nchans = meta.nchans.unwrap();
    let nsamp = meta.nsamples.unwrap();
    let shape = (nsamp as usize, nchans as usize);

    macro_rules! cast {
        ($ty: ident) => {
            Array::from_shape_vec(
                shape,
                raw.chunks_exact(nbits as usize / 8usize)
                    .map(|x| {
                        (match endian {
                            Endianness::Big => $ty::from_be_bytes,
                            Endianness::Little => $ty::from_le_bytes,
                            _ => unreachable!(),
                        })(x.try_into().unwrap())
                    })
                    .collect(),
            )
            .unwrap()
            .mapv(|x| x as f64)
            .reversed_axes()
        };
    }

    let data = match nbits {
        8 => match signed {
            Some(v) => {
                if v {
                    cast!(i8)
                } else {
                    cast!(u8)
                }
            }
            None => cast!(u8),
        },
        16 => cast!(u16),
        32 => cast!(f32),
        _ => unreachable!(),
    };

    Ok((data, endian, meta))
}

#[derive(Debug)]
pub struct SIGPROCFilterbank<'a> {
    pub data: Option<Array2<f64>>,
    pub endian: Option<Endianness>,
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
}

#[derive(Debug)]
pub struct SIGPROCTimeSeries<'a> {
    pub data: Option<Array1<f64>>,
    pub endian: Option<Endianness>,
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
}

impl<'a> SIGPROCFilterbank<'a> {
    pub fn from_bytes(i: &'a [u8]) -> Result<Self, PriwoError> {
        let (data, endian, meta) = parse(i)?;
        Ok(Self {
            data: Some(data),
            endian: Some(endian),
            filename: meta.filename,
            telescope_id: meta.telescope_id,
            telescope: meta.telescope,
            machine_id: meta.machine_id,
            data_type: meta.data_type,
            rawdatafile: meta.rawdatafile,
            source_name: meta.source_name,
            barycentric: meta.barycentric,
            pulsarcentric: meta.pulsarcentric,
            az_start: meta.az_start,
            za_start: meta.za_start,
            src_raj: meta.src_raj,
            src_dej: meta.src_dej,
            tstart: meta.tstart,
            tsamp: meta.tsamp,
            nbits: meta.nbits,
            nsamples: meta.nsamples,
            fch1: meta.fch1,
            foff: meta.foff,
            fchannel: meta.fchannel,
            nchans: meta.nchans,
            nifs: meta.nifs,
            refdm: meta.refdm,
            flux: meta.flux,
            period: meta.period,
            nbeams: meta.nbeams,
            ibeam: meta.ibeam,
            hdrlen: meta.hdrlen,
            pb: meta.pb,
            ecc: meta.ecc,
            asini: meta.asini,
            orig_hdrlen: meta.orig_hdrlen,
            new_hdrlen: meta.new_hdrlen,
            sampsize: meta.sampsize,
            bandwidth: meta.bandwidth,
            fbottom: meta.fbottom,
            ftop: meta.ftop,
            obs_date: meta.obs_date,
            obs_time: meta.obs_time,
            signed: meta.signed,
            accel: meta.accel,
        })
    }
}

impl<'a> SIGPROCTimeSeries<'a> {
    pub fn from_bytes(i: &'a [u8]) -> Result<Self, PriwoError> {
        let (data, endian, meta) = parse(i)?;
        Ok(Self {
            data: Some(Array::from_iter(data.iter().cloned())),
            endian: Some(endian),
            filename: meta.filename,
            telescope_id: meta.telescope_id,
            telescope: meta.telescope,
            machine_id: meta.machine_id,
            data_type: meta.data_type,
            rawdatafile: meta.rawdatafile,
            source_name: meta.source_name,
            barycentric: meta.barycentric,
            pulsarcentric: meta.pulsarcentric,
            az_start: meta.az_start,
            za_start: meta.za_start,
            src_raj: meta.src_raj,
            src_dej: meta.src_dej,
            tstart: meta.tstart,
            tsamp: meta.tsamp,
            nbits: meta.nbits,
            nsamples: meta.nsamples,
            fch1: meta.fch1,
            foff: meta.foff,
            fchannel: meta.fchannel,
            nchans: meta.nchans,
            nifs: meta.nifs,
            refdm: meta.refdm,
            flux: meta.flux,
            period: meta.period,
            nbeams: meta.nbeams,
            ibeam: meta.ibeam,
            hdrlen: meta.hdrlen,
            pb: meta.pb,
            ecc: meta.ecc,
            asini: meta.asini,
            orig_hdrlen: meta.orig_hdrlen,
            new_hdrlen: meta.new_hdrlen,
            sampsize: meta.sampsize,
            bandwidth: meta.bandwidth,
            fbottom: meta.fbottom,
            ftop: meta.ftop,
            obs_date: meta.obs_date,
            obs_time: meta.obs_time,
            signed: meta.signed,
            accel: meta.accel,
        })
    }
}

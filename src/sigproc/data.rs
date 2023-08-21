use super::SIGPROCMetadata;
use crate::err::PriwoError;
use ndarray::{Array, Array1, Array2};
use nom::number::Endianness;

struct SIGPROCData<'a> {
    data: Array2<f64>,
    endian: Endianness,
    meta: SIGPROCMetadata<'a>,
}

impl<'a> SIGPROCData<'a> {
    fn from_bytes(i: &'a [u8]) -> Result<Self, PriwoError> {
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

        Ok(Self { data, meta, endian })
    }
}

#[derive(Debug)]
pub struct SIGPROCFilterbank<'a> {
    pub data: Array2<f64>,
    pub endian: Endianness,
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
    pub data: Array1<f64>,
    pub endian: Endianness,
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
        let s = SIGPROCData::from_bytes(i)?;
        Ok(Self {
            data: s.data,
            endian: s.endian,
            filename: s.meta.filename,
            telescope_id: s.meta.telescope_id,
            telescope: s.meta.telescope,
            machine_id: s.meta.machine_id,
            data_type: s.meta.data_type,
            rawdatafile: s.meta.rawdatafile,
            source_name: s.meta.source_name,
            barycentric: s.meta.barycentric,
            pulsarcentric: s.meta.pulsarcentric,
            az_start: s.meta.az_start,
            za_start: s.meta.za_start,
            src_raj: s.meta.src_raj,
            src_dej: s.meta.src_dej,
            tstart: s.meta.tstart,
            tsamp: s.meta.tsamp,
            nbits: s.meta.nbits,
            nsamples: s.meta.nsamples,
            fch1: s.meta.fch1,
            foff: s.meta.foff,
            fchannel: s.meta.fchannel,
            nchans: s.meta.nchans,
            nifs: s.meta.nifs,
            refdm: s.meta.refdm,
            flux: s.meta.flux,
            period: s.meta.period,
            nbeams: s.meta.nbeams,
            ibeam: s.meta.ibeam,
            hdrlen: s.meta.hdrlen,
            pb: s.meta.pb,
            ecc: s.meta.ecc,
            asini: s.meta.asini,
            orig_hdrlen: s.meta.orig_hdrlen,
            new_hdrlen: s.meta.new_hdrlen,
            sampsize: s.meta.sampsize,
            bandwidth: s.meta.bandwidth,
            fbottom: s.meta.fbottom,
            ftop: s.meta.ftop,
            obs_date: s.meta.obs_date,
            obs_time: s.meta.obs_time,
            signed: s.meta.signed,
            accel: s.meta.accel,
        })
    }
}

impl<'a> SIGPROCTimeSeries<'a> {
    pub fn from_bytes(i: &'a [u8]) -> Result<Self, PriwoError> {
        let s = SIGPROCData::from_bytes(i)?;
        Ok(Self {
            data: Array::from_iter(s.data.iter().cloned()),
            endian: s.endian,
            filename: s.meta.filename,
            telescope_id: s.meta.telescope_id,
            telescope: s.meta.telescope,
            machine_id: s.meta.machine_id,
            data_type: s.meta.data_type,
            rawdatafile: s.meta.rawdatafile,
            source_name: s.meta.source_name,
            barycentric: s.meta.barycentric,
            pulsarcentric: s.meta.pulsarcentric,
            az_start: s.meta.az_start,
            za_start: s.meta.za_start,
            src_raj: s.meta.src_raj,
            src_dej: s.meta.src_dej,
            tstart: s.meta.tstart,
            tsamp: s.meta.tsamp,
            nbits: s.meta.nbits,
            nsamples: s.meta.nsamples,
            fch1: s.meta.fch1,
            foff: s.meta.foff,
            fchannel: s.meta.fchannel,
            nchans: s.meta.nchans,
            nifs: s.meta.nifs,
            refdm: s.meta.refdm,
            flux: s.meta.flux,
            period: s.meta.period,
            nbeams: s.meta.nbeams,
            ibeam: s.meta.ibeam,
            hdrlen: s.meta.hdrlen,
            pb: s.meta.pb,
            ecc: s.meta.ecc,
            asini: s.meta.asini,
            orig_hdrlen: s.meta.orig_hdrlen,
            new_hdrlen: s.meta.new_hdrlen,
            sampsize: s.meta.sampsize,
            bandwidth: s.meta.bandwidth,
            fbottom: s.meta.fbottom,
            ftop: s.meta.ftop,
            obs_date: s.meta.obs_date,
            obs_time: s.meta.obs_time,
            signed: s.meta.signed,
            accel: s.meta.accel,
        })
    }
}

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
        let (raw, endian, mut meta) = SIGPROCMetadata::from_bytes(i)?;

        if meta.nbits.is_none()
            && meta.nifs.is_none()
            && meta.nchans.is_none()
            && (meta.tsamp.is_none() && meta.sampsize.is_none())
        {
            return Err(PriwoError::InvalidMetadata);
        }

        if meta.data_type.unwrap() == 1
            && (meta.fch1.is_none() && meta.fbottom.is_none() && meta.ftop.is_none())
            && (meta.foff.is_none() && meta.fchannel.is_none() && meta.bandwidth.is_none())
        {
            return Err(PriwoError::InvalidMetadata);
        }

        if meta.data_type.unwrap() == 2 && meta.nifs.unwrap() != 1 && meta.nchans.unwrap() != 1 {
            return Err(PriwoError::InvalidMetadata);
        }

        let signed = meta.signed;
        let nifs = meta.nifs.unwrap();
        let nbits = meta.nbits.unwrap();
        let nchans = meta.nchans.unwrap();
        let nsamp = (raw.len() as u32 * 8) / nbits / nchans / nifs;
        meta.nsamples = Some(nsamp);

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

pub struct SIGPROCFilterbank<'a> {
    pub data: Array2<f64>,
    pub endian: Endianness,
    pub meta: SIGPROCMetadata<'a>,
}

pub struct SIGPROCTimeSeries<'a> {
    pub data: Array1<f64>,
    pub endian: Endianness,
    pub meta: SIGPROCMetadata<'a>,
}

impl<'a> SIGPROCFilterbank<'a> {
    pub fn from_bytes(i: &'a [u8]) -> Result<Self, PriwoError> {
        let s = SIGPROCData::from_bytes(i)?;
        Ok(Self {
            data: s.data,
            meta: s.meta,
            endian: s.endian,
        })
    }
}

impl<'a> SIGPROCTimeSeries<'a> {
    pub fn from_bytes(i: &'a [u8]) -> Result<Self, PriwoError> {
        let s = SIGPROCData::from_bytes(i)?;
        Ok(Self {
            meta: s.meta,
            endian: s.endian,
            data: Array::from_iter(s.data.iter().cloned()),
        })
    }
}

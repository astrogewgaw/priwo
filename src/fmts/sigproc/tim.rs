use super::SIGPROCHeader;
use crate::err::PriwoError;
use ndarray::{Array, Array1};
use nom::number::Endianness;

pub struct SIGPROCTimeSeries<'a> {
    pub data: Array1<f64>,
    pub endian: Endianness,
    pub header: SIGPROCHeader<'a>,
}

impl<'a> SIGPROCTimeSeries<'a> {
    pub fn from_bytes(i: &'a [u8]) -> Result<Self, PriwoError> {
        let (raw, endian, mut header) = SIGPROCHeader::from_bytes(i)?;

        if header.nbits.is_none()
            && header.nifs.is_none()
            && header.nchans.is_none()
            && (header.tsamp.is_none() && header.sampsize.is_none())
        {
            return Err(PriwoError::InvalidMetadata);
        }

        if header.nchans.unwrap() != 1 {
            return Err(PriwoError::InvalidMetadata);
        }

        let nbits = header.nbits.unwrap();
        let nsamp = (raw.len() as u32 * 8) / nbits;
        header.nsamples = Some(nsamp);

        macro_rules! cast {
            ($ty: ident) => {
                Array::from_vec(
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
                .mapv(|x| x as f64)
            };
        }

        let signed = header.signed;
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

        Ok(Self {
            data,
            endian,
            header,
        })
    }
}

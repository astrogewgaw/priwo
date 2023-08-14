use super::SIGPROCHeader;
use crate::err::PriwoError;
use ndarray::{Array, Array2};
use nom::number::Endianness;

pub struct SIGPROCFilterbank<'a> {
    pub data: Array2<f64>,
    pub endian: Endianness,
    pub header: SIGPROCHeader<'a>,
}

impl<'a> SIGPROCFilterbank<'a> {
    pub fn from_bytes(i: &'a [u8]) -> Result<Self, PriwoError> {
        let (raw, endian, mut header) = SIGPROCHeader::from_bytes(i)?;

        if header.nbits.is_none()
            && header.nifs.is_none()
            && header.nchans.is_none()
            && (header.tsamp.is_none() && header.sampsize.is_none())
            && (header.fch1.is_none() && header.fbottom.is_none() && header.ftop.is_none())
            && (header.foff.is_none() && header.fchannel.is_none() && header.bandwidth.is_none())
        {
            return Err(PriwoError::InvalidMetadata);
        }

        let nifs = header.nifs.unwrap();
        let nbits = header.nbits.unwrap();
        let nchans = header.nchans.unwrap();
        let nsamp = (raw.len() as u32 * 8) / nbits / nchans / nifs;
        header.nsamples = Some(nsamp);

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

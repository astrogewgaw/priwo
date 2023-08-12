use super::SIGPROCHeader;
use crate::err::PriwoError;
use numpy::ndarray::{Array, Array2};

pub struct SIGPROCFilterbank<'a> {
    pub raw: &'a [u8],
    pub data: Array2<f32>,
    pub header: SIGPROCHeader<'a>,
}

impl<'a> SIGPROCFilterbank<'a> {
    pub fn from_bytes(i: &'a [u8]) -> Result<Self, PriwoError> {
        let (raw, header) = SIGPROCHeader::from_bytes(i)?;

        let nf = header.nchans.unwrap() as usize;
        let nt = header.nsamples.unwrap() as usize;
        let data = raw.iter().map(|x| *x as f32).collect();
        let data = Array::from_shape_vec((nt, nf), data).unwrap();

        Ok(Self { raw, data, header })
    }
}

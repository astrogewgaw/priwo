use super::SIGPROCHeader;
use crate::err::PriwoError;
use nom::number::Endianness;

pub struct SIGPROCTimeSeries<'a> {
    pub raw: &'a [u8],
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

        let nbits = header.nbits.unwrap();
        let nsamp = (i.len() as u32 * 8) / nbits;
        header.nsamples = Some(nsamp);

        Ok(Self {
            raw,
            endian,
            header,
        })
    }
}

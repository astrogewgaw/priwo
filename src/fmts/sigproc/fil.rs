use super::SIGPROCHeader;
use crate::err::PriwoError;
use nom::number::Endianness;

pub struct SIGPROCFilterbank<'a> {
    pub raw: &'a [u8],
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
        let nsamp = (i.len() as u32 * 8) / nbits / nchans / nifs;
        header.nsamples = Some(nsamp);

        Ok(Self {
            raw,
            endian,
            header,
        })
    }
}

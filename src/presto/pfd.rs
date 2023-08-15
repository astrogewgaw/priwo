#[cfg(feature = "python")]
use dict_derive::{FromPyObject, IntoPyObject};

#[derive(Debug)]
#[cfg_attr(feature = "python", derive(FromPyObject, IntoPyObject))]
pub struct PRESTOFoldedData<'a> {
    pub ndms: Option<u32>,
    pub nperiods: Option<u32>,
    pub npdots: Option<u32>,
    pub nsub: Option<u32>,
    pub npart: Option<u32>,
    pub nbin: Option<u32>,
    pub nchan: Option<u32>,
    pub pstep: Option<u32>,
    pub pdstep: Option<u32>,
    pub dmstep: Option<u32>,
    pub ndmfact: Option<u32>,
    pub npfact: Option<u32>,
    pub filename: Option<&'a str>,
    pub candname: Option<&'a str>,
    pub telescope: Option<&'a str>,
    pub pgdev: Option<&'a str>,
    pub ra: Option<&'a str>,
    pub dec: Option<&'a str>,
    pub dt: Option<f64>,
    pub t0: Option<f64>,
    pub tn: Option<f64>,
    pub tepoch: Option<f64>,
    pub bepoch: Option<f64>,
    pub vavg: Option<f64>,
    pub f0: Option<f64>,
    pub df: Option<f64>,
    pub bestdm: Option<f64>,
    pub power: Option<f64>,
    pub p: Option<f64>,
    pub pd: Option<f64>,
    pub pdd: Option<f64>,
    pub pb: Option<f64>,
    pub e: Option<f64>,
    pub x: Option<f64>,
    pub w: Option<f64>,
    pub t: Option<f64>,
    pub pbd: Option<f64>,
    pub wd: Option<f64>,
}

impl<'a> PRESTOFoldedData<'a> {
    pub fn from_bytes() {}
}

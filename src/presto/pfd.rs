use nom::{
    bytes::streaming::take,
    combinator::{map_res, peek},
    multi::{count, length_data},
    number::streaming::{f64, u32},
    number::Endianness,
    IResult,
};

use ndarray::{Array, Array1, Array3};
use std::cmp::Ordering;

use crate::err::PriwoError;

type ParseResult<'a, T> = IResult<&'a [u8], T, PriwoError>;

fn prestr(i: &[u8], endian: Endianness) -> ParseResult<&str> {
    let (i, s) = map_res(length_data(u32(endian)), std::str::from_utf8)(i)?;
    Ok((i, s))
}

fn padstr(i: &[u8]) -> ParseResult<&str> {
    let (i, s) = map_res(take(16usize), std::str::from_utf8)(i)?;
    Ok((i, s.trim_end_matches(char::from(0))))
}

enum Field<'a> {
    Ndms(u32),
    Nperiods(u32),
    Npdots(u32),
    Nsub(u32),
    Npart(u32),
    Nbin(u32),
    Nchan(u32),
    Pstep(u32),
    Pdstep(u32),
    Dmstep(u32),
    Ndmfact(u32),
    Npfact(u32),
    Filename(&'a str),
    Candname(&'a str),
    Telescope(&'a str),
    Pgdev(&'a str),
    Ra(&'a str),
    Dec(&'a str),
    Dt(f64),
    T0(f64),
    Tn(f64),
    Tepoch(f64),
    Bepoch(f64),
    Vavg(f64),
    F0(f64),
    Df(f64),
    Bestdm(f64),
    TopoPower(f64),
    TopoP(f64),
    TopoPd(f64),
    TopoPdd(f64),
    BaryPower(f64),
    BaryP(f64),
    BaryPd(f64),
    BaryPdd(f64),
    FoldPower(f64),
    FoldP(f64),
    FoldPd(f64),
    FoldPdd(f64),
    OrbP(f64),
    OrbE(f64),
    OrbX(f64),
    OrbW(f64),
    OrbT(f64),
    OrbPd(f64),
    OrbWd(f64),
}

fn parse(i: &[u8]) -> ParseResult<'_, (Endianness, Vec<Field<'_>>)> {
    let (i, dummy) = peek(count(u32(Endianness::Little), 5))(i)?;
    let endian = match dummy.iter().max().unwrap().cmp(&10000) {
        Ordering::Greater => Endianness::Big,
        _ => Endianness::Little,
    };

    let (i, ndms) = u32(endian)(i)?;
    let (i, nperiods) = u32(endian)(i)?;
    let (i, npdots) = u32(endian)(i)?;
    let (i, nsub) = u32(endian)(i)?;
    let (i, npart) = u32(endian)(i)?;
    let (i, nbin) = u32(endian)(i)?;
    let (i, nchan) = u32(endian)(i)?;
    let (i, pstep) = u32(endian)(i)?;
    let (i, pdstep) = u32(endian)(i)?;
    let (i, dmstep) = u32(endian)(i)?;
    let (i, ndmfact) = u32(endian)(i)?;
    let (i, npfact) = u32(endian)(i)?;
    let (i, filename) = prestr(i, endian)?;
    let (i, candname) = prestr(i, endian)?;
    let (i, telescope) = prestr(i, endian)?;
    let (i, pgdev) = prestr(i, endian)?;
    let (i, ra) = padstr(i)?;
    let (i, dec) = padstr(i)?;
    let (i, dt) = f64(endian)(i)?;
    let (i, t0) = f64(endian)(i)?;
    let (i, tn) = f64(endian)(i)?;
    let (i, tepoch) = f64(endian)(i)?;
    let (i, bepoch) = f64(endian)(i)?;
    let (i, vavg) = f64(endian)(i)?;
    let (i, f0) = f64(endian)(i)?;
    let (i, df) = f64(endian)(i)?;
    let (i, bestdm) = f64(endian)(i)?;
    let (i, topo_power) = f64(endian)(i)?;
    let (i, topo_p) = f64(endian)(i)?;
    let (i, topo_pd) = f64(endian)(i)?;
    let (i, topo_pdd) = f64(endian)(i)?;
    let (i, bary_power) = f64(endian)(i)?;
    let (i, bary_p) = f64(endian)(i)?;
    let (i, bary_pd) = f64(endian)(i)?;
    let (i, bary_pdd) = f64(endian)(i)?;
    let (i, fold_power) = f64(endian)(i)?;
    let (i, fold_p) = f64(endian)(i)?;
    let (i, fold_pd) = f64(endian)(i)?;
    let (i, fold_pdd) = f64(endian)(i)?;
    let (i, orb_p) = f64(endian)(i)?;
    let (i, orb_e) = f64(endian)(i)?;
    let (i, orb_x) = f64(endian)(i)?;
    let (i, orb_w) = f64(endian)(i)?;
    let (i, orb_t) = f64(endian)(i)?;
    let (i, orb_pd) = f64(endian)(i)?;
    let (i, orb_wd) = f64(endian)(i)?;

    Ok((
        i,
        (
            endian,
            vec![
                Field::Ndms(ndms),
                Field::Nperiods(nperiods),
                Field::Npdots(npdots),
                Field::Nsub(nsub),
                Field::Npart(npart),
                Field::Nbin(nbin),
                Field::Nchan(nchan),
                Field::Pstep(pstep),
                Field::Pdstep(pdstep),
                Field::Dmstep(dmstep),
                Field::Ndmfact(ndmfact),
                Field::Npfact(npfact),
                Field::Filename(filename),
                Field::Candname(candname),
                Field::Telescope(telescope),
                Field::Pgdev(pgdev),
                Field::Ra(ra),
                Field::Dec(dec),
                Field::Dt(dt),
                Field::T0(t0),
                Field::Tn(tn),
                Field::Tepoch(tepoch),
                Field::Bepoch(bepoch),
                Field::Vavg(vavg),
                Field::F0(f0),
                Field::Df(df),
                Field::Bestdm(bestdm),
                Field::TopoPower(topo_power),
                Field::TopoP(topo_p),
                Field::TopoPd(topo_pd),
                Field::TopoPdd(topo_pdd),
                Field::BaryPower(bary_power),
                Field::BaryP(bary_p),
                Field::BaryPd(bary_pd),
                Field::BaryPdd(bary_pdd),
                Field::FoldPower(fold_power),
                Field::FoldP(fold_p),
                Field::FoldPd(fold_pd),
                Field::FoldPdd(fold_pdd),
                Field::OrbP(orb_p),
                Field::OrbE(orb_e),
                Field::OrbX(orb_x),
                Field::OrbW(orb_w),
                Field::OrbT(orb_t),
                Field::OrbPd(orb_pd),
                Field::OrbWd(orb_wd),
            ],
        ),
    ))
}

#[derive(Debug, Default)]
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
    pub topo_power: Option<f64>,
    pub topo_p: Option<f64>,
    pub topo_pd: Option<f64>,
    pub topo_pdd: Option<f64>,
    pub bary_power: Option<f64>,
    pub bary_p: Option<f64>,
    pub bary_pd: Option<f64>,
    pub bary_pdd: Option<f64>,
    pub fold_power: Option<f64>,
    pub fold_p: Option<f64>,
    pub fold_pd: Option<f64>,
    pub fold_pdd: Option<f64>,
    pub orb_p: Option<f64>,
    pub orb_e: Option<f64>,
    pub orb_x: Option<f64>,
    pub orb_w: Option<f64>,
    pub orb_t: Option<f64>,
    pub orb_pd: Option<f64>,
    pub orb_wd: Option<f64>,
    pub dms: Option<Array1<f64>>,
    pub periods: Option<Array1<f64>>,
    pub pdots: Option<Array1<f64>>,
    pub data: Option<Array3<f64>>,
    pub stats: Option<Array3<f64>>,
    pub endian: Option<Endianness>,
}

impl<'a> PRESTOFoldedData<'a> {
    pub fn from_bytes(i: &'a [u8]) -> Result<Self, PriwoError> {
        let (i, (endian, fields)) = parse(i).map_err(|e| match e {
            nom::Err::Incomplete(_) => PriwoError::IncompleteMetadata,
            nom::Err::Error(e) => e,
            nom::Err::Failure(e) => e,
        })?;

        let mut s = Self::default();

        for field in fields {
            match field {
                Field::Ndms(x) => s.ndms = Some(x),
                Field::Nperiods(x) => s.nperiods = Some(x),
                Field::Npdots(x) => s.npdots = Some(x),
                Field::Nsub(x) => s.nsub = Some(x),
                Field::Npart(x) => s.npart = Some(x),
                Field::Nbin(x) => s.nbin = Some(x),
                Field::Nchan(x) => s.nchan = Some(x),
                Field::Pstep(x) => s.pstep = Some(x),
                Field::Pdstep(x) => s.pdstep = Some(x),
                Field::Dmstep(x) => s.dmstep = Some(x),
                Field::Ndmfact(x) => s.ndmfact = Some(x),
                Field::Npfact(x) => s.npfact = Some(x),
                Field::Filename(x) => s.filename = Some(x),
                Field::Candname(x) => s.candname = Some(x),
                Field::Telescope(x) => s.telescope = Some(x),
                Field::Pgdev(x) => s.pgdev = Some(x),
                Field::Ra(x) => s.ra = Some(x),
                Field::Dec(x) => s.dec = Some(x),
                Field::Dt(x) => s.dt = Some(x),
                Field::T0(x) => s.t0 = Some(x),
                Field::Tn(x) => s.tn = Some(x),
                Field::Tepoch(x) => s.tepoch = Some(x),
                Field::Bepoch(x) => s.bepoch = Some(x),
                Field::Vavg(x) => s.vavg = Some(x),
                Field::F0(x) => s.f0 = Some(x),
                Field::Df(x) => s.df = Some(x),
                Field::Bestdm(x) => s.bestdm = Some(x),
                Field::TopoPower(x) => s.topo_power = Some(x),
                Field::TopoP(x) => s.topo_p = Some(x),
                Field::TopoPd(x) => s.topo_pd = Some(x),
                Field::TopoPdd(x) => s.topo_pdd = Some(x),
                Field::BaryPower(x) => s.bary_power = Some(x),
                Field::BaryP(x) => s.bary_p = Some(x),
                Field::BaryPd(x) => s.bary_pd = Some(x),
                Field::BaryPdd(x) => s.bary_pdd = Some(x),
                Field::FoldPower(x) => s.fold_power = Some(x),
                Field::FoldP(x) => s.fold_p = Some(x),
                Field::FoldPd(x) => s.fold_pd = Some(x),
                Field::FoldPdd(x) => s.fold_pdd = Some(x),
                Field::OrbP(x) => s.orb_p = Some(x),
                Field::OrbE(x) => s.orb_e = Some(x),
                Field::OrbX(x) => s.orb_x = Some(x),
                Field::OrbW(x) => s.orb_w = Some(x),
                Field::OrbT(x) => s.orb_t = Some(x),
                Field::OrbPd(x) => s.orb_pd = Some(x),
                Field::OrbWd(x) => s.orb_wd = Some(x),
            }
        }

        s.endian = Some(endian);

        let nbin = s.nbin.unwrap() as usize;
        let nsub = s.nsub.unwrap() as usize;
        let ndms = s.ndms.unwrap() as usize;
        let npart = s.npart.unwrap() as usize;
        let npdots = s.npdots.unwrap() as usize;
        let nperiods = s.nperiods.unwrap() as usize;

        let (dms, i) = i.split_at(ndms * 8);
        let (periods, i) = i.split_at(nperiods * 8);
        let (pdots, i) = i.split_at(npdots * 8);
        let (data, i) = i.split_at(npart * nsub * nbin * 8);

        s.dms = Some(Array::from_vec(
            dms.to_vec()
                .chunks_exact(8)
                .map(|x| {
                    (match endian {
                        Endianness::Big => f64::from_be_bytes,
                        Endianness::Little => f64::from_le_bytes,
                        _ => unreachable!(),
                    })(x.try_into().unwrap())
                })
                .collect(),
        ));

        s.periods = Some(Array::from_vec(
            periods
                .to_vec()
                .chunks_exact(8)
                .map(|x| {
                    (match endian {
                        Endianness::Big => f64::from_be_bytes,
                        Endianness::Little => f64::from_le_bytes,
                        _ => unreachable!(),
                    })(x.try_into().unwrap())
                })
                .collect(),
        ));

        s.pdots = Some(Array::from_vec(
            pdots
                .to_vec()
                .chunks_exact(8)
                .map(|x| {
                    (match endian {
                        Endianness::Big => f64::from_be_bytes,
                        Endianness::Little => f64::from_le_bytes,
                        _ => unreachable!(),
                    })(x.try_into().unwrap())
                })
                .collect(),
        ));

        s.data = Some(
            Array::from_shape_vec(
                (npart, nsub, nbin),
                data.to_vec()
                    .chunks_exact(8)
                    .map(|x| {
                        (match endian {
                            Endianness::Big => f64::from_be_bytes,
                            Endianness::Little => f64::from_le_bytes,
                            _ => unreachable!(),
                        })(x.try_into().unwrap())
                    })
                    .collect(),
            )
            .unwrap(),
        );

        s.stats = Some(
            Array::from_shape_vec(
                (7, nsub, npart),
                i.to_vec()
                    .chunks_exact(8)
                    .map(|x| {
                        (match endian {
                            Endianness::Big => f64::from_be_bytes,
                            Endianness::Little => f64::from_le_bytes,
                            _ => unreachable!(),
                        })(x.try_into().unwrap())
                    })
                    .collect(),
            )
            .unwrap(),
        );

        Ok(s)
    }
}

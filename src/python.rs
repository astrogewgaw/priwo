use crate::presto::PRESTOFoldedData;
use crate::sigproc::{SIGPROCFilterbank, SIGPROCMetadata, SIGPROCTimeSeries};
use numpy::{IntoPyArray, PyArray1, PyArray2};
use pyo3::prelude::*;
use pyo3::types::PyDict;

#[pyfunction]
fn _parsehdr<'py>(py: Python<'py>, i: &[u8]) -> PyResult<&'py PyDict> {
    let dict = PyDict::new(py);
    let (_, _, hdr) = SIGPROCMetadata::from_bytes(i).unwrap();

    dict.set_item("filename", hdr.filename.into_py(py))?;
    dict.set_item("telescope_id", hdr.telescope_id.into_py(py))?;
    dict.set_item("telescope", hdr.telescope.into_py(py))?;
    dict.set_item("machine_id", hdr.machine_id.into_py(py))?;
    dict.set_item("data_type", hdr.data_type.into_py(py))?;
    dict.set_item("rawdatafile", hdr.rawdatafile.into_py(py))?;
    dict.set_item("source_name", hdr.source_name.into_py(py))?;
    dict.set_item("barycentric", hdr.barycentric.into_py(py))?;
    dict.set_item("pulsarcentric", hdr.pulsarcentric.into_py(py))?;
    dict.set_item("az_start", hdr.az_start.into_py(py))?;
    dict.set_item("za_start", hdr.za_start.into_py(py))?;
    dict.set_item("src_raj", hdr.src_raj.into_py(py))?;
    dict.set_item("src_dej", hdr.src_dej.into_py(py))?;
    dict.set_item("tstart", hdr.tstart.into_py(py))?;
    dict.set_item("tsamp", hdr.tsamp.into_py(py))?;
    dict.set_item("nbits", hdr.nbits.into_py(py))?;
    dict.set_item("nsamples", hdr.nsamples.into_py(py))?;
    dict.set_item("fch1", hdr.fch1.into_py(py))?;
    dict.set_item("foff", hdr.foff.into_py(py))?;
    dict.set_item("fchannel", hdr.fchannel.into_py(py))?;
    dict.set_item("nchans", hdr.nchans.into_py(py))?;
    dict.set_item("nifs", hdr.nifs.into_py(py))?;
    dict.set_item("refdm", hdr.refdm.into_py(py))?;
    dict.set_item("flux", hdr.flux.into_py(py))?;
    dict.set_item("period", hdr.period.into_py(py))?;
    dict.set_item("nbeams", hdr.nbeams.into_py(py))?;
    dict.set_item("ibeam", hdr.ibeam.into_py(py))?;
    dict.set_item("hdrlen", hdr.hdrlen.into_py(py))?;
    dict.set_item("pb", hdr.pb.into_py(py))?;
    dict.set_item("ecc", hdr.ecc.into_py(py))?;
    dict.set_item("asini", hdr.asini.into_py(py))?;
    dict.set_item("orig_hdrlen", hdr.orig_hdrlen.into_py(py))?;
    dict.set_item("new_hdrlen", hdr.new_hdrlen.into_py(py))?;
    dict.set_item("sampsize", hdr.sampsize.into_py(py))?;
    dict.set_item("bandwidth", hdr.bandwidth.into_py(py))?;
    dict.set_item("fbottom", hdr.fbottom.into_py(py))?;
    dict.set_item("ftop", hdr.ftop.into_py(py))?;
    dict.set_item("obs_date", hdr.obs_date.into_py(py))?;
    dict.set_item("obs_time", hdr.obs_time.into_py(py))?;
    dict.set_item("signed", hdr.signed.into_py(py))?;
    dict.set_item("accel", hdr.accel.into_py(py))?;

    Ok(dict)
}

#[pyfunction]
fn _parsefil<'py>(py: Python<'py>, i: &'py [u8]) -> PyResult<(&'py PyDict, &'py PyArray2<f64>)> {
    let dict = PyDict::new(py);
    let fil = SIGPROCFilterbank::from_bytes(i).unwrap();

    let data = fil.data;
    let data = data.into_pyarray(py);

    dict.set_item("filename", fil.filename.into_py(py))?;
    dict.set_item("telescope_id", fil.telescope_id.into_py(py))?;
    dict.set_item("telescope", fil.telescope.into_py(py))?;
    dict.set_item("machine_id", fil.machine_id.into_py(py))?;
    dict.set_item("data_type", fil.data_type.into_py(py))?;
    dict.set_item("rawdatafile", fil.rawdatafile.into_py(py))?;
    dict.set_item("source_name", fil.source_name.into_py(py))?;
    dict.set_item("barycentric", fil.barycentric.into_py(py))?;
    dict.set_item("pulsarcentric", fil.pulsarcentric.into_py(py))?;
    dict.set_item("az_start", fil.az_start.into_py(py))?;
    dict.set_item("za_start", fil.za_start.into_py(py))?;
    dict.set_item("src_raj", fil.src_raj.into_py(py))?;
    dict.set_item("src_dej", fil.src_dej.into_py(py))?;
    dict.set_item("tstart", fil.tstart.into_py(py))?;
    dict.set_item("tsamp", fil.tsamp.into_py(py))?;
    dict.set_item("nbits", fil.nbits.into_py(py))?;
    dict.set_item("nsamples", fil.nsamples.into_py(py))?;
    dict.set_item("fch1", fil.fch1.into_py(py))?;
    dict.set_item("foff", fil.foff.into_py(py))?;
    dict.set_item("fchannel", fil.fchannel.into_py(py))?;
    dict.set_item("nchans", fil.nchans.into_py(py))?;
    dict.set_item("nifs", fil.nifs.into_py(py))?;
    dict.set_item("refdm", fil.refdm.into_py(py))?;
    dict.set_item("flux", fil.flux.into_py(py))?;
    dict.set_item("period", fil.period.into_py(py))?;
    dict.set_item("nbeams", fil.nbeams.into_py(py))?;
    dict.set_item("ibeam", fil.ibeam.into_py(py))?;
    dict.set_item("hdrlen", fil.hdrlen.into_py(py))?;
    dict.set_item("pb", fil.pb.into_py(py))?;
    dict.set_item("ecc", fil.ecc.into_py(py))?;
    dict.set_item("asini", fil.asini.into_py(py))?;
    dict.set_item("orig_hdrlen", fil.orig_hdrlen.into_py(py))?;
    dict.set_item("new_hdrlen", fil.new_hdrlen.into_py(py))?;
    dict.set_item("sampsize", fil.sampsize.into_py(py))?;
    dict.set_item("bandwidth", fil.bandwidth.into_py(py))?;
    dict.set_item("fbottom", fil.fbottom.into_py(py))?;
    dict.set_item("ftop", fil.ftop.into_py(py))?;
    dict.set_item("obs_date", fil.obs_date.into_py(py))?;
    dict.set_item("obs_time", fil.obs_time.into_py(py))?;
    dict.set_item("signed", fil.signed.into_py(py))?;
    dict.set_item("accel", fil.accel.into_py(py))?;

    Ok((dict, data))
}

#[pyfunction]
fn _parsetim<'py>(py: Python<'py>, i: &'py [u8]) -> PyResult<(&'py PyDict, &'py PyArray1<f64>)> {
    let dict = PyDict::new(py);
    let tim = SIGPROCTimeSeries::from_bytes(i).unwrap();

    let data = tim.data;
    let data = data.into_pyarray(py);

    dict.set_item("filename", tim.filename.into_py(py))?;
    dict.set_item("telescope_id", tim.telescope_id.into_py(py))?;
    dict.set_item("telescope", tim.telescope.into_py(py))?;
    dict.set_item("machine_id", tim.machine_id.into_py(py))?;
    dict.set_item("data_type", tim.data_type.into_py(py))?;
    dict.set_item("rawdatafile", tim.rawdatafile.into_py(py))?;
    dict.set_item("source_name", tim.source_name.into_py(py))?;
    dict.set_item("barycentric", tim.barycentric.into_py(py))?;
    dict.set_item("pulsarcentric", tim.pulsarcentric.into_py(py))?;
    dict.set_item("az_start", tim.az_start.into_py(py))?;
    dict.set_item("za_start", tim.za_start.into_py(py))?;
    dict.set_item("src_raj", tim.src_raj.into_py(py))?;
    dict.set_item("src_dej", tim.src_dej.into_py(py))?;
    dict.set_item("tstart", tim.tstart.into_py(py))?;
    dict.set_item("tsamp", tim.tsamp.into_py(py))?;
    dict.set_item("nbits", tim.nbits.into_py(py))?;
    dict.set_item("nsamples", tim.nsamples.into_py(py))?;
    dict.set_item("fch1", tim.fch1.into_py(py))?;
    dict.set_item("foff", tim.foff.into_py(py))?;
    dict.set_item("fchannel", tim.fchannel.into_py(py))?;
    dict.set_item("nchans", tim.nchans.into_py(py))?;
    dict.set_item("nifs", tim.nifs.into_py(py))?;
    dict.set_item("refdm", tim.refdm.into_py(py))?;
    dict.set_item("flux", tim.flux.into_py(py))?;
    dict.set_item("period", tim.period.into_py(py))?;
    dict.set_item("nbeams", tim.nbeams.into_py(py))?;
    dict.set_item("ibeam", tim.ibeam.into_py(py))?;
    dict.set_item("hdrlen", tim.hdrlen.into_py(py))?;
    dict.set_item("pb", tim.pb.into_py(py))?;
    dict.set_item("ecc", tim.ecc.into_py(py))?;
    dict.set_item("asini", tim.asini.into_py(py))?;
    dict.set_item("orig_hdrlen", tim.orig_hdrlen.into_py(py))?;
    dict.set_item("new_hdrlen", tim.new_hdrlen.into_py(py))?;
    dict.set_item("sampsize", tim.sampsize.into_py(py))?;
    dict.set_item("bandwidth", tim.bandwidth.into_py(py))?;
    dict.set_item("fbottom", tim.fbottom.into_py(py))?;
    dict.set_item("ftop", tim.ftop.into_py(py))?;
    dict.set_item("obs_date", tim.obs_date.into_py(py))?;
    dict.set_item("obs_time", tim.obs_time.into_py(py))?;
    dict.set_item("signed", tim.signed.into_py(py))?;
    dict.set_item("accel", tim.accel.into_py(py))?;

    Ok((dict, data))
}

#[pyfunction]
fn _parsepfd<'py>(py: Python<'py>, i: &[u8]) -> PyResult<&'py PyDict> {
    let dict = PyDict::new(py);
    let (_, pfd) = PRESTOFoldedData::from_bytes(i).unwrap();

    dict.set_item("ndms", pfd.ndms.into_py(py))?;
    dict.set_item("nperiods", pfd.nperiods.into_py(py))?;
    dict.set_item("npdots", pfd.npdots.into_py(py))?;
    dict.set_item("nsub", pfd.nsub.into_py(py))?;
    dict.set_item("npart", pfd.npart.into_py(py))?;
    dict.set_item("nbin", pfd.nbin.into_py(py))?;
    dict.set_item("nchan", pfd.nchan.into_py(py))?;
    dict.set_item("pstep", pfd.pstep.into_py(py))?;
    dict.set_item("pdstep", pfd.pdstep.into_py(py))?;
    dict.set_item("dmstep", pfd.dmstep.into_py(py))?;
    dict.set_item("ndmfact", pfd.ndmfact.into_py(py))?;
    dict.set_item("npfact", pfd.npfact.into_py(py))?;
    dict.set_item("filename", pfd.filename.into_py(py))?;
    dict.set_item("candname", pfd.candname.into_py(py))?;
    dict.set_item("telescope", pfd.telescope.into_py(py))?;
    dict.set_item("pgdev", pfd.pgdev.into_py(py))?;
    dict.set_item("ra", pfd.ra.into_py(py))?;
    dict.set_item("dec", pfd.dec.into_py(py))?;
    dict.set_item("dt", pfd.dt.into_py(py))?;
    dict.set_item("t0", pfd.t0.into_py(py))?;
    dict.set_item("tn", pfd.tn.into_py(py))?;
    dict.set_item("tepoch", pfd.tepoch.into_py(py))?;
    dict.set_item("bepoch", pfd.bepoch.into_py(py))?;
    dict.set_item("vavg", pfd.vavg.into_py(py))?;
    dict.set_item("f0", pfd.f0.into_py(py))?;
    dict.set_item("df", pfd.df.into_py(py))?;
    dict.set_item("bestdm", pfd.bestdm.into_py(py))?;
    dict.set_item("topo_power", pfd.topo_power.into_py(py))?;
    dict.set_item("topo_p", pfd.topo_p.into_py(py))?;
    dict.set_item("topo_pd", pfd.topo_pd.into_py(py))?;
    dict.set_item("topo_pdd", pfd.topo_pdd.into_py(py))?;
    dict.set_item("bary_power", pfd.bary_power.into_py(py))?;
    dict.set_item("bary_p", pfd.bary_p.into_py(py))?;
    dict.set_item("bary_pd", pfd.bary_pd.into_py(py))?;
    dict.set_item("bary_pdd", pfd.bary_pdd.into_py(py))?;
    dict.set_item("fold_power", pfd.fold_power.into_py(py))?;
    dict.set_item("fold_p", pfd.fold_p.into_py(py))?;
    dict.set_item("fold_pd", pfd.fold_pd.into_py(py))?;
    dict.set_item("fold_pdd", pfd.fold_pdd.into_py(py))?;
    dict.set_item("pb", pfd.pb.into_py(py))?;
    dict.set_item("e", pfd.e.into_py(py))?;
    dict.set_item("x", pfd.x.into_py(py))?;
    dict.set_item("w", pfd.w.into_py(py))?;
    dict.set_item("t", pfd.t.into_py(py))?;
    dict.set_item("pbd", pfd.pbd.into_py(py))?;
    dict.set_item("wd", pfd.wd.into_py(py))?;

    Ok(dict)
}

#[pymodule]
#[pyo3(name = "_internals")]
fn _internals(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(_parsehdr, m)?)?;
    m.add_function(wrap_pyfunction!(_parsefil, m)?)?;
    m.add_function(wrap_pyfunction!(_parsetim, m)?)?;
    m.add_function(wrap_pyfunction!(_parsepfd, m)?)?;
    Ok(())
}

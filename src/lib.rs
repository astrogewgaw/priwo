mod err;
mod fmts;

use ndarray::Array;
use numpy::{IntoPyArray, PyArray1, PyArray2};

use pyo3::prelude::*;

use crate::fmts::sigproc::{SIGPROCFilterbank, SIGPROCHeader, SIGPROCTimeSeries};

#[pyfunction]
fn _parsehdr(i: &[u8]) -> PyResult<SIGPROCHeader> {
    let (_, _, hdr) = SIGPROCHeader::from_bytes(i).unwrap();
    Ok(hdr)
}

#[pyfunction]
fn _parsefil<'py>(
    py: Python<'py>,
    i: &'py [u8],
) -> PyResult<(SIGPROCHeader<'py>, &'py PyArray2<f32>)> {
    let fil = SIGPROCFilterbank::from_bytes(i).unwrap();

    let meta = fil.header;
    let nf = meta.nchans.unwrap() as usize;
    let nt = meta.nsamples.unwrap() as usize;
    let data = fil.raw.iter().map(|x| *x as f32).collect();
    let data = Array::from_shape_vec((nt, nf), data).unwrap();
    let data = data.into_pyarray(py);

    Ok((meta, data))
}

#[pyfunction]
fn _parsetim<'py>(
    py: Python<'py>,
    i: &'py [u8],
) -> PyResult<(SIGPROCHeader<'py>, &'py PyArray1<f32>)> {
    let tim = SIGPROCTimeSeries::from_bytes(i).unwrap();

    let meta = tim.header;
    let data = tim.raw.iter().map(|x| *x as f32).collect();
    let data = Array::from_vec(data);
    let data = data.into_pyarray(py);

    Ok((meta, data))
}

#[pymodule]
#[pyo3(name = "_internals")]
fn _internals(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(_parsehdr, m)?)?;
    m.add_function(wrap_pyfunction!(_parsefil, m)?)?;
    m.add_function(wrap_pyfunction!(_parsetim, m)?)?;
    Ok(())
}

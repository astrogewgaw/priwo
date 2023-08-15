mod err;
mod sigproc;

use crate::sigproc::{SIGPROCFilterbank, SIGPROCMetadata, SIGPROCTimeSeries};
use numpy::{IntoPyArray, PyArray1, PyArray2};
use pyo3::prelude::*;

#[pyfunction]
fn _parsehdr(i: &[u8]) -> PyResult<SIGPROCMetadata> {
    let (_, _, hdr) = SIGPROCMetadata::from_bytes(i).unwrap();
    Ok(hdr)
}

#[pyfunction]
fn _parsefil<'py>(
    py: Python<'py>,
    i: &'py [u8],
) -> PyResult<(SIGPROCMetadata<'py>, &'py PyArray2<f64>)> {
    let fil = SIGPROCFilterbank::from_bytes(i).unwrap();

    let data = fil.data;
    let meta = fil.meta;
    let data = data.into_pyarray(py);

    Ok((meta, data))
}

#[pyfunction]
fn _parsetim<'py>(
    py: Python<'py>,
    i: &'py [u8],
) -> PyResult<(SIGPROCMetadata<'py>, &'py PyArray1<f64>)> {
    let tim = SIGPROCTimeSeries::from_bytes(i).unwrap();

    let data = tim.data;
    let meta = tim.meta;
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

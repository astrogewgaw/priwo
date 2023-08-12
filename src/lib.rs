mod err;
#[allow(dead_code)]
mod fmts;

use numpy::{IntoPyArray, PyArray2};
use pyo3::prelude::*;
use pyo3::Python;

use fmts::sigproc::{SIGPROCFilterbank, SIGPROCHeader};

#[pyfunction]
fn _parsehdr(i: &[u8]) -> PyResult<SIGPROCHeader> {
    let (_, hdr) = SIGPROCHeader::from_bytes(i).unwrap();
    Ok(hdr)
}

#[pyfunction]
fn _parsefil<'py>(
    py: Python<'py>,
    i: &'py [u8],
) -> PyResult<(SIGPROCHeader<'py>, &'py PyArray2<f32>)> {
    let fil = SIGPROCFilterbank::from_bytes(i).unwrap();

    let data = fil.data;
    let meta = fil.header;
    let fil = data.into_pyarray(py);

    Ok((meta, fil))
}

#[pymodule]
#[pyo3(name = "_internals")]
fn _internals(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(_parsehdr, m)?)?;
    m.add_function(wrap_pyfunction!(_parsefil, m)?)?;
    Ok(())
}

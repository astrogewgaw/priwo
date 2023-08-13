use nom::error::{FromExternalError, ParseError};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum PriwoError {
    #[error("Invalid metadata.")]
    InvalidMetadata,
    #[error("Incomplete metadata.")]
    IncompleteMetadata,
    #[error("Unknown parsing error.")]
    UnknownParsingError,
    #[error("External parsing error.")]
    ExternalParsingError(String),
}

impl<I> ParseError<I> for PriwoError {
    fn from_error_kind(_input: I, _kind: nom::error::ErrorKind) -> Self {
        PriwoError::UnknownParsingError
    }

    fn append(_: I, _: nom::error::ErrorKind, other: Self) -> Self {
        other
    }
}

impl<I, E> FromExternalError<I, E> for PriwoError
where
    E: std::error::Error,
{
    fn from_external_error(_input: I, _kind: nom::error::ErrorKind, e: E) -> Self {
        PriwoError::ExternalParsingError(format!("{}", e))
    }
}

"""
R/W PSRFITS files.

For the complete PSRFITS specification, see:

1. https://www.atnf.csiro.au/research/pulsar/psrfits_definition/Psrfits.html
2. https://www.atnf.csiro.au/research/pulsar/psrfits_definition/PsrfitsDocumentation.html.
"""

from construct import (
    this,
    Int,
    Short,
    Select,
    Single,
    Double,
    Struct,
    Aligned,
    RepeatUntil,
    PaddedString,
)


### Header Unit Definition. ###


header = """
    Struct to parse an ASCII formatted `Header Unit` in a FITS file.
    Each header unit is a multiple of 2880 bytes long. If necessary, 
    the header unit is padded out to the required length with ASCII 
    blanks.

    Each header unit contains a sequence of fixed-length 80-character 
    keyword records which have the general form:

        KEYNAME = value / comment string

    The keyword names may be up to 8 characters long and can only contain 
    uppercase letters A to Z, the digits 0 to 9, the hyphen (-), and the 
    underscore character (_). The keyword name is (usually) followed by 
    an equals sign and a space character in columns 9 and 10 of the record, 
    followed by the value of the keyword which may be either an integer, a 
    floating point number, a complex value (i.e., a pair of numbers), a 
    character string (enclosed in single quotes), or a Boolean value (the 
    letter T or F). Some keywords, (e.g., COMMENT and HISTORY) are not 
    followed by an equals sign and in that case columns 9 - 80 of the record 
    may contain any string of ASCII text.

    The last keyword in the header is always the `END' keyword which has 
    blank value and comment fields. The header is padded with additional 
    blank records if necessary so that it is a multiple of 2880 bytes 
    (equivalent to 36 80-byte keywords) long. Note that the header unit 
    may only contain ASCII text characters ranging from hexadecimal 20 
    to 7E); non-printing ASCII characters such as tabs, carriage-returns, 
    or line-feeds are not allowed anywhere within the header unit.

    (Specification taken from: https://fits.gsfc.nasa.gov/fits_primer.html)
    """ * Aligned(
    2880,
    RepeatUntil(
        lambda obj, _, __: obj.strip() == "END",
        PaddedString(80, "ascii"),
    ),
)


### Extension HDU Definitions. ###


history = """
    History Binary Table Extension.

    Contains a history of the file processing operations with
    key parameters following each operation, with one line per
    operation.
    """ * Struct(
    "proc_date" / PaddedString(24, "ascii"),
    "proc_cmd" / PaddedString(256, "ascii"),
    "scale" / PaddedString(8, "ascii"),
    "pol_type" / PaddedString(8, "ascii"),
    "nsub" / Int,
    "npol" / Short,
    "nbin" / Short,
    "nbin_prd" / Short,
    "tbin" / Double,
    "cfreq" / Double,
    "nchan" / Int,
    "chanbw" / Double,
    "ref_freq" / Double,
    "dm" / Double,
    "rm" / Double,
    "pr_corr" / Short,
    "fd_corr" / Short,
    "be_corr" / Short,
    "rm_corr" / Short,
    "dedisp" / Short,
    "dedisp_method" / PaddedString(32, "ascii"),
    "sc_method" / PaddedString(32, "ascii"),
    "calib_method" / PaddedString(32, "ascii"),
    "calib_file" / PaddedString(256, "ascii"),
    "rfi_method" / PaddedString(32, "ascii"),
    "rm_model" / PaddedString(32, "ascii"),
    "aux_rm_c" / Short,
    "dm_model" / PaddedString(32, "ascii"),
    "aux_dm_c" / Short,
)


obsdescr = """
    Observation Description Binary Table Extension.

    This is a free-format ascii table which can contain
    any desired information about the observation and/or
    its processing.""" * Struct(
    "descr" / PaddedString(128, "ascii")
)


psrparam = """
    Ephemeris Binary Table Extension.

    The pulsar ephemeris file used to form the polyco
    or predictor file for data folding.""" * Struct(
    "param" / PaddedString(128, "ascii")
)


polyco = """
    TEMPO1 Polyco History Binary Table Extension.

    A table of the polyco parameters used for each stage
    of the processing. Check out the Tempo documentation
    (http://tempo.sourceforge.net/) for a description of the
    parameters and the algorithm for pulse phase prediction.""" * Struct(
    "proc_date" / PaddedString(24, "ascii"),
    "poly_ver" / PaddedString(16, "ascii"),
    "nspan" / Short,
    "ncoeff" / Short,
    "num_block" / Short,
    "nsite" / PaddedString(8, "ascii"),
    "ref_freq" / Double,
    "pred_phase" / Double,
    "ref_mjd" / Double,
    "ref_phase" / Double,
    "ref_f0" / Double,
    "log_fit_err" / Double,
    "coeff" / Double[this.ncoeff],
)


t2predict = """
    TEMPO2 Predictor Binary Table Extension.

    Table used by Tempo2 for prediction of pulse phases.
    The table consists of a two-dimensional (time and
    frequency) array of Chebyshev basis functions along
    with header parameters. See the Tempo2 documentation
    (http://www.atnf.csiro.au/research/pulsar/tempo2) for
    a description of the predictor file and how to make
    use of it.""" * Struct(
    "predict" / PaddedString(128, "ascii")
)


cohddisp = """
    Coherent Dedispersion Parameters Binary Table Extension.

    Table describing the details of the coherent dedispersion
    processing applied to (sub)band data.
    """ * Struct(
    "cfreq" / Double,
    "bandwidth" / Double,
    "out_nchan" / Int,
    "out_freq" / Double[this.out_nchan],
    "out_bandwidth" / Select(Double, Double[this.out_nchan]),
    "nchirp" / Select(Int, Int[this.out_nchan]),
    "ncyc_pos" / Select(Int, Int[this.out_nchan]),
    "ncyc_neg" / Select(Int, Int[this.out_nchan]),
)


bandpass = """
    Original Bandpass Binary Table Extension

    Table recording the input power spectrum for each polarisation channel.
    """ * Struct(
    "dat_offs" / Single,
    "dat_scl" / Single,
    "data" / Short,
)


flux_cal = (
    """
    Flux Calibration Data Binary Table Extension

    Table giving spectra of the system noise and the injected calibration
    signal and their uncertainties for each polarisation channel. Channel
    centre frequencies and weights are also recorded. These data are normally
    obtained by recording the injected calibration signal pointing on and off
    a standard flux-calibration source (e.g. Hydra A). They are only available
    after processing of calibration observations, for example, using the PSRCHIVE
    program "fluxcal".
    """
    * Struct()
)


calpoln = (
    """
    Artificial Calibrator Stokes Parameters Binary Table Extension

    Fractional polarisation of the injected calibration signal, expressed
    as spectra of Stokes Q/I, U/I and V/I.
    """
    * Struct()
)


feedpar = (
    """
    Feed Cross-Coupling Parameters Binary Table Extension

    Table of feed cross-coupling parameters used to correct for the
    effects of coupling between nominally orthogonal feeds. They are
    normally measured by analysing a set of observations of a strong
    pulsar over a wide range of parallactic angles using, for example,
    the PSRCHIVE program PCM.
    """
    * Struct()
)


speckurt = (
    """
    Spectral Kurtosis Binary Table Extension

    This table contains statistics relating to RFI excision using the
    spectral kurtosis method (Nita & Gary 2010), as implemented (for
    example) by the data analysis program DSPSR.
    """
    * Struct()
)


subint = (
    """
    Subintegration data Binary Table Extension

    Table containing the observed power spectra, that is spectra after
    detection or multiplication. Two modes of observation are catered
    for:

    *   fold mode:      where the data are synchronously folded at the
                        apparent period of a pulsar using a Tempo polyco
                        file or a Tempo2 predictor file and samples are
                        binned in pulse phase

    *   search mode:    where streamed multichannel data are recorded in
                        successive samples.

    In both modes, the data can have a single polarisation (normally the
    sum of two orthogonal polarisations), two orthogonal polarisations or
    all four polarisation spectra.

    In fold mode, data are summed over a sub-integration time and successive
    sub-integrations are stored in successive rows of the BINTABLE. In search
    mode, data are blocked in groups of NSBLK samples and stored in successive
    rows of the BINTABLE. To avoid excessive overheads, NSBLK is typically 4096.

    Fold-mode data are stored as 16-bit signed integers with elements of the
    data array in bin, channel and polarisation order with the pulse profile
    bins in contiguous locations. Before conversion to integers, the mean
    channel power (averaged over bins and polarisations) during the
    sub-integration is subtracted from the channel data and the residual is
    scaled so that the values in the DATA array cover the whole available
    range (-32768 to 32767). The original observed powers are reconstructed
    using:

        Real value = DATA value * DAT_SCL + DAT_OFFS.

    Search-mode data may be stored as 1-bit, 2-bit, 4-bit or 8-bit signed or
    unsigned integers and are written as a byte array. Data digitised with
    less than 8 bits are packed with earlier samples in higher-order bits of
    the byte (i.e., "big-endian"). Elements of the data array are in channel,
    polarisation and sample order with the spectral channels in contiguous
    locations.

    Prior to few-bit digitisation, search-mode sample spectra are generally
    normalised and given zero mean by forming (S-R)/R, where S is the
    observed spectrum and R is an estimate of the bandpass or reference
    spectrum. This effectively does a bandpass calibration and gives an
    approximately constant rms deviation across the spectrum in order to
    optimise the few-bit digitisation. These data are normally analysed
    directly without application of the scale factors and offsets. If
    required, the reference spectrum may be reconstructed from the DAT_OFFS
    and DAT_SCL fields of the table. However note that, if channel running
    means are used to form the reference spectrum, the recorded values are
    sampled at sub-integration intervals and do do not necessarily represent
    the exact values used to form the recorded spectra.

    When unsigned integers are used to record the truncated data, a zero offset
    (ZERO_OFFS) is added to the digitised value. Normally ZERO_OFFS = 2^(NBIT - 1)
    - 0.5, but for total-intensity multi-bit data, a smaller value may be used
    to give more headroom. The original observed values are reconstructed using:

        Real value = (DATA value - ZERO_OFFS) * DAT_SCL + DAT_OFFS.

    The output data for long search-mode observations may be split in time or
    frequency and recorded in separate files to keep file sizes at manageable
    values. It is assumed that the data sampling is continuous across the split
    files.
    """
    * Struct()
)


dig_stat = (
    """
    Digitiser Statistics Binary Table Extension

    A table of digitiser parameters sampled at regular intervals,
    for example, each correlator cycle. For example, for each cycle,
    the mean and rms levels of the digitised signal for each input
    polarisation channel could be recorded.
    """
    * Struct()
)


dig_cnts = (
    """
    Digitiser Counts Binary Table Extension

    A table containing histograms of occurrence of digitised
    sample values for each polarisation or digitiser channel
    integrated over some period, e.g., a correlator cycle.
    Table values are offset and scaled to cover the full range
    of a 16-bit signed integer. The original histogram values
    are reconstructed using:

        Histogram value = DATA table value * DAT_SCL + DAT_OFFS.
    """
    * Struct()
)


def read_psrfits():

    """"""

    pass


def write_psrfits():

    """"""

    pass
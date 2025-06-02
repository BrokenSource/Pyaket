use crate::*;

/// Writes a tar stream of data to a directory
fn unpack_tar<R: Read>(decoder: R, path: &Path) -> Result<()> {
    tar::Archive::new(decoder).unpack(path)?;
    Ok(())
}

/// Unpack common archive formats to a directory
pub fn unpack_bytes(
    bytes: &Vec<u8>,
    path:  impl AsRef<Path>,
    flag:  Option<&str>,
) -> Result<()> {

    // Unique identifer for unpacked data
    let hash = xxh3_64(bytes).to_string();
    let flag = path.as_ref()
        .join(flag.unwrap_or("archive"))
        .with_extension("unpack");

    // Detect different data or partial unpacks,
    // skip if the data is already unpacked
    if let Ok(data) = read_string(&flag) {
        if data == hash {
            return Ok(());
        } else {
            rmdir(&path)?;
        }
    }

    #[cfg(feature="zstd")]
    use zstd::stream::read::Decoder as ZsDecoder;
    #[cfg(feature="bzip2")]
    use bzip2::read::BzDecoder;
    use flate2::read::GzDecoder;
    use zip::ZipArchive;

    logging::info!("Unpacking ({})", path.as_ref().display());

    // Identify the archive format by the magic bytes
    let mut cursor = Cursor::new(bytes.as_slice());
    let mut magic = [0u8; 6];
    cursor.read_exact(&mut magic)?;
    cursor.seek(SeekFrom::Start(0))?;
    match magic {
        [0x50, 0x4B, 0x03, 0x04, ..] => ZipArchive::new(cursor)?.extract(path.as_ref())?,
        #[cfg(feature="zstd")]
        [0x28, 0xB5, 0x2F, 0xFD, ..] => unpack_tar(ZsDecoder::new(cursor)?, path.as_ref())?,
        #[cfg(feature="bzip2")]
        [0x42, 0x5A, ..            ] => unpack_tar(BzDecoder::new(cursor),  path.as_ref())?,
        [0x1F, 0x8B, ..            ] => unpack_tar(GzDecoder::new(cursor),  path.as_ref())?,
        _ => bail!("Unknown archive format for magic bytes: {:?}", magic),
    }
    write(flag, hash)?;
    Ok(())
}

/// Unpack common archive formats from a file to a directory
pub fn unpack_file(
    file: impl AsRef<Path>,
    path: impl AsRef<Path>,
    flag: Option<&str>,
) -> Result<()> {
    archive::unpack_bytes(&read(file)?, path, flag)
}

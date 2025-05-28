use crate::*;

pub struct Network;

impl Network {

    /// Check if URL is reachable and returns a 200 OK status
    pub fn exists(url: &str) -> Result<bool, ureq::Error> {
        let response = ureq::head(url).call()?;
        Ok(response.status().is_success())
    }

    /// Syntactic sugar for `bail!` on `!exists(url)`
    pub fn must_exist(url: &str) -> Result<()> {
        if !Network::exists(url)? {
            bail!("Download url is not valid: {}", url)}
        Ok(())
    }

    /// In-memory download an url to a byte vector
    pub fn download_bytes(url: &str) -> Result<Vec<u8>> {
        logging::info!("Downloading ({})", url);

        Ok(ureq::get(url).call()?.body_mut()
            .with_config().limit(100 * 1024 * 1024)
            .read_to_vec()?)
    }

    /// Download to a file serving as cache, returns the bytes
    pub fn download_file(url: &str, path: &PathBuf) -> Result<Vec<u8>> {
        match path.exists() {
            true => Ok(read(path)?),
            false => {
                // Note: The trick here is that rename is atomic!
                let bytes = Network::download_bytes(&url)?;
                let temp = path.with_extension("part");
                mkdir(&path.parent().unwrap())?;
                write(&temp, &bytes)?;
                rename(&temp, &path)?;
                Ok(bytes)
            }
        }
    }

    /// Smart download to a path or in-memory
    pub fn download(url: &str, path: Option<&PathBuf>) -> Result<Vec<u8>> {
        match path {
            Some(path) => Network::download_file(&url, path),
            None => Network::download_bytes(&url),
        }
    }
}

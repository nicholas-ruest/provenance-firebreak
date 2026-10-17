//! CLI input validation helpers (DDD-12).
pub fn safe_state_path(path: &std::path::Path) -> bool {
    !path.as_os_str().is_empty()
        && !path
            .components()
            .any(|c| matches!(c, std::path::Component::ParentDir))
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn traversal() {
        assert!(!safe_state_path(std::path::Path::new("../x")));
    }
}

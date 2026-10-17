//! Split-conformal risk control (ADR-003, ADR-014, DDD-03).
use serde::{Deserialize, Serialize};
use thiserror::Error;
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Calibrator {
    scores: Vec<f64>,
    alpha: f64,
}
#[derive(Debug, Error)]
pub enum CalibrationError {
    #[error("need scores in [0,1] and alpha in (0,1)")]
    Invalid,
}
impl Calibrator {
    pub fn fit(mut scores: Vec<f64>, alpha: f64) -> Result<Self, CalibrationError> {
        if scores.is_empty()
            || !(0.0..1.0).contains(&alpha)
            || scores.iter().any(|x| !(0.0..=1.0).contains(x))
        {
            return Err(CalibrationError::Invalid);
        }
        scores.sort_by(f64::total_cmp);
        Ok(Self { scores, alpha })
    }
    pub fn upper(&self, point: f64) -> f64 {
        let n = self.scores.len();
        let rank = (((n + 1) as f64 * (1.0 - self.alpha)).ceil() as usize).clamp(1, n) - 1;
        (point + self.scores[rank]).min(1.0)
    }
    pub fn coverage_target(&self) -> f64 {
        1.0 - self.alpha
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn finite_sample() {
        let c = Calibrator::fit(vec![0.1, 0.2, 0.3, 0.4], 0.2).unwrap();
        assert_eq!(c.upper(0.7), 1.0);
    }
}

from typing import Dict, Any, List


class PerformanceAnalyticsAgent:
    def analyze_performance_trends(
        self,
        current_period_data: Dict[str, float],
        previous_period_data: Dict[str, float],
        period_label: str = "28D"
    ) -> Dict[str, Any]:
        """
        Compares GSC/GA4 metrics across periods (1D, 7D, 28D) and triggers significant change alerts.
        """
        alerts: List[str] = []
        metrics_summary: Dict[str, Any] = {}

        for metric in ["clicks", "impressions", "sessions"]:
            curr = current_period_data.get(metric, 0.0)
            prev = previous_period_data.get(metric, 0.0)

            pct_change = ((curr - prev) / prev * 100) if prev > 0 else (100.0 if curr > 0 else 0.0)
            metrics_summary[metric] = {
                "current": curr,
                "previous": prev,
                "pct_change": round(pct_change, 2)
            }

            if pct_change <= -20.0:
                alerts.append(f"CRITICAL DROP: {metric.capitalize()} dropped by {abs(pct_change):.1f}% over {period_label}.")
            elif pct_change >= 20.0:
                alerts.append(f"SIGNIFICANT SPIKE: {metric.capitalize()} increased by {pct_change:.1f}% over {period_label}.")

        return {
            "period": period_label,
            "metrics": metrics_summary,
            "has_alerts": len(alerts) > 0,
            "alerts": alerts
        }
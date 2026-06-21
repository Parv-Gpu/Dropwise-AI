import { useRef, useState } from "react";
import axios from "axios";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar, Doughnut, Pie } from "react-chartjs-2";
import "./App.css";

const API_BASE_URL = "https://dropwise-ai-backend.onrender.com";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend
);

function App() {
  const dashboardRef = useRef(null);

  const [datasetFile, setDatasetFile] = useState(null);
  const [datasetResult, setDatasetResult] = useState(null);
  const [singleResult, setSingleResult] = useState(null);
  const [selectedSession, setSelectedSession] = useState(null);

  const [loading, setLoading] = useState(false);
  const [pdfLoading, setPdfLoading] = useState(false);

  const [searchId, setSearchId] = useState("");
  const [sessionSearchId, setSessionSearchId] = useState("");

  const [reasonFilter, setReasonFilter] = useState("all");
  const [confidenceFilter, setConfidenceFilter] = useState("all");
  const [deviceFilter, setDeviceFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");
  const [page, setPage] = useState(1);

  const PAGE_SIZE = 20;

  const chartColors = [
    "#2563eb",
    "#16a34a",
    "#f97316",
    "#7c3aed",
    "#dc2626",
    "#0891b2",
    "#ca8a04",
    "#475569",
  ];

  const formatLabel = (text) => String(text || "-").replaceAll("_", " ");

  const objectToChartData = (obj, label = "Count") => ({
    labels: Object.keys(obj || {}).map(formatLabel),
    datasets: [
      {
        label,
        data: Object.values(obj || {}),
        backgroundColor: chartColors,
        borderRadius: 8,
        barThickness: 24,
        maxBarThickness: 28,
      },
    ],
  });

  const horizontalBarOptions = {
    responsive: true,
    maintainAspectRatio: false,
    devicePixelRatio: window.devicePixelRatio || 2,
    indexAxis: "y",
    plugins: {
      legend: { display: false },
      tooltip: { enabled: true },
    },
    scales: {
      x: {
        beginAtZero: true,
        ticks: { color: "#475569" },
        grid: { color: "#e5e7eb" },
      },
      y: {
        ticks: { color: "#475569" },
        grid: { display: false },
      },
    },
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    devicePixelRatio: window.devicePixelRatio || 2,
    plugins: {
      legend: {
        position: "right",
        labels: { color: "#475569", font: { weight: "600" } },
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const value = context.raw;
            const percent = total ? Math.round((value / total) * 100) : 0;
            return `${context.label}: ${value} (${percent}%)`;
          },
        },
      },
    },
  };

  const analyzeDataset = async () => {
    if (!datasetFile) {
      alert("Please select JSONL dataset file");
      return;
    }

    const formData = new FormData();
    formData.append("file", datasetFile);

    try {
      setLoading(true);

      const response = await axios.post(
        `${API_BASE_URL}/upload-dataset`,
        formData
      );

      setDatasetResult(response.data);
      setSingleResult(null);
      setSelectedSession(null);
      setSessionSearchId("");
      setPage(1);
    } catch (error) {
      console.error(error);
      alert("Dataset analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const analyzeSingleSession = () => {
    if (!datasetResult?.results) {
      alert("Please analyze full dataset first");
      return;
    }

    if (!sessionSearchId.trim()) {
      alert("Please enter Session ID or User ID");
      return;
    }

    const query = sessionSearchId.trim().toLowerCase();

    const found = datasetResult.results.find(
      (item) =>
        item.session_id?.toLowerCase() === query ||
        item.user_id?.toLowerCase() === query
    );

    if (!found) {
      alert("Session ID or User ID not found in analyzed dataset");
      return;
    }

    setSingleResult(found);
    setSelectedSession(found);
  };

  const resetPage = () => setPage(1);

  const filteredResults =
    datasetResult?.results?.filter((item) => {
      const search = searchId.toLowerCase();

      const matchesSearch =
        item.session_id?.toLowerCase().includes(search) ||
        item.user_id?.toLowerCase().includes(search);

      const matchesReason =
        reasonFilter === "all" || item.predicted_reason === reasonFilter;

      const matchesConfidence =
        confidenceFilter === "all" ||
        item.confidence_level === confidenceFilter;

      const matchesDevice =
        deviceFilter === "all" || item.device === deviceFilter;

      const matchesStatus =
        statusFilter === "all" ||
        (statusFilter === "correct" && item.is_correct) ||
        (statusFilter === "review" && !item.is_correct);

      return (
        matchesSearch &&
        matchesReason &&
        matchesConfidence &&
        matchesDevice &&
        matchesStatus
      );
    }) || [];

  const totalPages = Math.max(1, Math.ceil(filteredResults.length / PAGE_SIZE));
  const currentPage = Math.min(page, totalPages);

  const paginatedResults = filteredResults.slice(
    (currentPage - 1) * PAGE_SIZE,
    currentPage * PAGE_SIZE
  );

  const startRow =
    filteredResults.length === 0 ? 0 : (currentPage - 1) * PAGE_SIZE + 1;

  const endRow = Math.min(currentPage * PAGE_SIZE, filteredResults.length);

  const uniqueReasons = Object.keys(datasetResult?.reason_distribution || {});
  const uniqueDevices = Object.keys(datasetResult?.device_distribution || {});

  const getMaxEntry = (obj) => {
    const entries = Object.entries(obj || {});
    if (!entries.length) return ["-", 0];
    return entries.reduce((max, item) => (item[1] > max[1] ? item : max));
  };

  const getMinEntry = (obj) => {
    const entries = Object.entries(obj || {});
    if (!entries.length) return ["-", 0];
    return entries.reduce((min, item) => (item[1] < min[1] ? item : min));
  };

  const topDropoff = getMaxEntry(datasetResult?.reason_distribution);
  const mostReview = getMaxEntry(datasetResult?.review_count_by_reason);
  const lowestConfidence = getMinEntry(datasetResult?.avg_confidence_by_reason);
  const bestCategory = getMaxEntry(datasetResult?.category_accuracy);

  const predictionStatus = datasetResult
    ? {
        Correct: datasetResult.correct_predictions,
        "Review Needed": datasetResult.wrong_predictions,
      }
    : {};

  const funnelData = datasetResult
    ? {
        "Total Sessions": datasetResult.total_sessions,
        Correct: datasetResult.correct_predictions,
        "High Confidence": datasetResult.confidence_distribution?.high || 0,
        "Review Needed": datasetResult.wrong_predictions,
      }
    : {};

  const recommendationsByReason = {
    price_concern: "Show total cost, shipping, and discounts earlier.",
    trust_concern:
      "Add stronger reviews, return policy visibility, and trust badges.",
    product_fit_concern:
      "Improve size guide, images, fit information, and return clarity.",
    checkout_friction: "Enable guest checkout and reduce form/login steps.",
    delivery_concern:
      "Show delivery estimates and pincode availability on product pages.",
    product_information_gap:
      "Improve product descriptions, FAQs, images, and material details.",
    comparison_shopping:
      "Add comparison tables and highlight unique selling points.",
    low_purchase_intent:
      "Improve product discovery and retarget users with relevant offers.",
  };

  const aiSummary = datasetResult
    ? [
        `${Math.round(
          (topDropoff[1] / datasetResult.total_sessions) * 100
        )}% users dropped due to ${formatLabel(topDropoff[0])}.`,
        `${mostReview[1]} sessions need manual review, mostly from ${formatLabel(
          mostReview[0]
        )}.`,
        `${formatLabel(
          lowestConfidence[0]
        )} has the lowest average confidence at ${Math.round(
          lowestConfidence[1] * 100
        )}%.`,
        `Recommended Action: ${
          recommendationsByReason[topDropoff[0]] ||
          "Review customer sessions and improve product-page clarity."
        }`,
      ]
    : [];

  const heatmapReasons = Object.keys(datasetResult?.reason_distribution || {});
  const heatmapLevels = ["high", "medium", "low"];

  const heatmapData = {};
  let maxHeatmapValue = 1;

  datasetResult?.results?.forEach((item) => {
    const reason = item.predicted_reason || "unknown";
    const level = item.confidence_level || "unknown";

    if (!heatmapData[reason]) heatmapData[reason] = {};
    heatmapData[reason][level] = (heatmapData[reason][level] || 0) + 1;

    maxHeatmapValue = Math.max(maxHeatmapValue, heatmapData[reason][level]);
  });

  const getHeatColor = (value) => {
    const intensity = value / maxHeatmapValue;
    if (intensity >= 0.75) return "#2563eb";
    if (intensity >= 0.45) return "#60a5fa";
    if (intensity >= 0.2) return "#bfdbfe";
    return "#eff6ff";
  };

  const exportPDF = async () => {
    if (!dashboardRef.current || !datasetResult) return;

    try {
      setPdfLoading(true);

      const canvas = await html2canvas(dashboardRef.current, {
        scale: 2,
        backgroundColor: "#f5f7fb",
      });

      const imgData = canvas.toDataURL("image/png");
      const pdf = new jsPDF("p", "mm", "a4");

      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();

      pdf.setFontSize(20);
      pdf.text("DropWise AI Brand Report", 14, 18);

      pdf.setFontSize(11);
      pdf.text(`Accuracy: ${datasetResult.accuracy}%`, 14, 28);
      pdf.text(`Total Sessions: ${datasetResult.total_sessions}`, 14, 35);
      pdf.text(`Top Reason: ${formatLabel(topDropoff[0])}`, 14, 42);
      pdf.text(
        `Recommended Action: ${
          recommendationsByReason[topDropoff[0]] || "Review sessions manually."
        }`,
        14,
        49
      );

      const imgWidth = pageWidth - 20;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;

      let heightLeft = imgHeight;
      let position = 58;

      pdf.addImage(imgData, "PNG", 10, position, imgWidth, imgHeight);
      heightLeft -= pageHeight - position;

      while (heightLeft > 0) {
        pdf.addPage();
        position = heightLeft - imgHeight + 10;
        pdf.addImage(imgData, "PNG", 10, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;
      }

      pdf.save("DropWise_AI_Brand_Report.pdf");
    } catch (error) {
      console.error(error);
      alert("PDF export failed");
    } finally {
      setPdfLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>DropWise AI</h1>
        <p>Customer Drop-off Intelligence Dashboard for Brand Owners</p>
      </header>

      <h2 className="section-title">Dataset Dashboard</h2>

      <div className="upload-card">
        <input
          type="file"
          accept=".jsonl"
          onChange={(e) => setDatasetFile(e.target.files[0])}
        />

        <button onClick={analyzeDataset}>
          {loading ? "Analyzing..." : "Analyze Full Dataset"}
        </button>
      </div>

      {datasetResult && (
        <>
          <div className="export-row">
            <button onClick={exportPDF}>
              {pdfLoading ? "Generating PDF..." : "Generate Brand Report PDF"}
            </button>
          </div>

          <div ref={dashboardRef}>
            <div className="stats-grid">
              <div className="stat-card">
                <span>Total Sessions</span>
                <h3>{datasetResult.total_sessions}</h3>
              </div>

              <div className="stat-card">
                <span>Accuracy</span>
                <h3>{datasetResult.accuracy}%</h3>
              </div>

              <div className="stat-card">
                <span>Correct</span>
                <h3>{datasetResult.correct_predictions}</h3>
              </div>

              <div className="stat-card">
                <span>Review Needed</span>
                <h3>{datasetResult.wrong_predictions}</h3>
              </div>

              <div className="stat-card">
                <span>Avg Confidence</span>
                <h3>{Math.round(datasetResult.avg_confidence * 100)}%</h3>
              </div>

              <div className="stat-card">
                <span>Unique Reasons</span>
                <h3>{datasetResult.unique_reasons}</h3>
              </div>
            </div>

            <div className="ai-summary-card">
              <h3>AI Dataset Summary</h3>
              <ul>
                {aiSummary.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>

            <div className="insights-grid">
              <div className="insight-card">
                <span>Top Drop-off Reason</span>
                <h3>{formatLabel(topDropoff[0])}</h3>
                <p>{topDropoff[1]} sessions</p>
              </div>

              <div className="insight-card">
                <span>Most Review Needed</span>
                <h3>{formatLabel(mostReview[0])}</h3>
                <p>{mostReview[1]} sessions</p>
              </div>

              <div className="insight-card">
                <span>Lowest Confidence Reason</span>
                <h3>{formatLabel(lowestConfidence[0])}</h3>
                <p>{Math.round(lowestConfidence[1] * 100)}%</p>
              </div>

              <div className="insight-card">
                <span>Best Performing Category</span>
                <h3>{formatLabel(bestCategory[0])}</h3>
                <p>{bestCategory[1]}% accuracy</p>
              </div>
            </div>

            <div className="top-chart-grid">
              <div className="chart-card reason-chart-card">
                <h3>Drop-off Reason Distribution</h3>

                <div className="chart-box reason-chart-box">
                  <Bar
                    data={objectToChartData(
                      datasetResult.reason_distribution,
                      "Sessions"
                    )}
                    options={horizontalBarOptions}
                  />
                </div>
              </div>

              <div className="side-charts">
                <div className="chart-card">
                  <h3>Confidence Split</h3>

                  <div className="chart-box small-chart">
                    <Doughnut
                      data={objectToChartData(
                        datasetResult.confidence_distribution
                      )}
                      options={pieOptions}
                    />
                  </div>
                </div>

                <div className="chart-card">
                  <h3>Prediction Status</h3>

                  <div className="chart-box small-chart">
                    <Doughnut
                      data={objectToChartData(predictionStatus)}
                      options={pieOptions}
                    />
                  </div>
                </div>
              </div>
            </div>

            <div className="dashboard-grid">
              <div className="chart-card">
                <h3>Category-wise Accuracy</h3>
                <div className="chart-box">
                  <Bar
                    data={objectToChartData(
                      datasetResult.category_accuracy,
                      "Accuracy %"
                    )}
                    options={horizontalBarOptions}
                  />
                </div>
              </div>

              <div className="chart-card">
                <h3>Average Confidence by Reason</h3>
                <div className="chart-box">
                  <Bar
                    data={objectToChartData(
                      datasetResult.avg_confidence_by_reason,
                      "Confidence"
                    )}
                    options={horizontalBarOptions}
                  />
                </div>
              </div>

              <div className="chart-card">
                <h3>Secondary Reason Distribution</h3>
                <div className="chart-box">
                  <Bar
                    data={objectToChartData(
                      datasetResult.secondary_reason_distribution,
                      "Sessions"
                    )}
                    options={horizontalBarOptions}
                  />
                </div>
              </div>

              <div className="chart-card">
                <h3>Device Distribution</h3>
                <div className="chart-box">
                  <Pie
                    data={objectToChartData(datasetResult.device_distribution)}
                    options={pieOptions}
                  />
                </div>
              </div>

              <div className="chart-card">
                <h3>Review Count by Reason</h3>
                <div className="chart-box">
                  <Bar
                    data={objectToChartData(
                      datasetResult.review_count_by_reason,
                      "Reviews"
                    )}
                    options={horizontalBarOptions}
                  />
                </div>
              </div>

              <div className="chart-card">
                <h3>Model Funnel</h3>
                <div className="chart-box">
                  <Bar
                    data={objectToChartData(funnelData, "Sessions")}
                    options={horizontalBarOptions}
                  />
                </div>
              </div>
            </div>

            <div className="heatmap-card">
              <h3>Reason vs Confidence Heatmap</h3>

              <div className="heatmap-table">
                <div className="heatmap-header">Reason</div>

                {heatmapLevels.map((level) => (
                  <div className="heatmap-header" key={level}>
                    {formatLabel(level)}
                  </div>
                ))}

                {heatmapReasons.map((reason) => (
                  <div className="heatmap-row" key={reason}>
                    <div className="heatmap-reason">{formatLabel(reason)}</div>

                    {heatmapLevels.map((level) => {
                      const value = heatmapData[reason]?.[level] || 0;

                      return (
                        <div
                          key={`${reason}-${level}`}
                          className="heatmap-cell"
                          style={{ background: getHeatColor(value) }}
                        >
                          {value}
                        </div>
                      );
                    })}
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="filters-card">
            <input
              type="text"
              placeholder="Search Session ID or User ID"
              value={searchId}
              onChange={(e) => {
                setSearchId(e.target.value);
                resetPage();
              }}
            />

            <select
              value={reasonFilter}
              onChange={(e) => {
                setReasonFilter(e.target.value);
                resetPage();
              }}
            >
              <option value="all">All Primary Reasons</option>
              {uniqueReasons.map((reason) => (
                <option key={reason} value={reason}>
                  {reason}
                </option>
              ))}
            </select>

            <select
              value={confidenceFilter}
              onChange={(e) => {
                setConfidenceFilter(e.target.value);
                resetPage();
              }}
            >
              <option value="all">All Confidence</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>

            <select
              value={deviceFilter}
              onChange={(e) => {
                setDeviceFilter(e.target.value);
                resetPage();
              }}
            >
              <option value="all">All Devices</option>
              {uniqueDevices.map((device) => (
                <option key={device} value={device}>
                  {device}
                </option>
              ))}
            </select>

            <select
              value={statusFilter}
              onChange={(e) => {
                setStatusFilter(e.target.value);
                resetPage();
              }}
            >
              <option value="all">All Status</option>
              <option value="correct">Correct</option>
              <option value="review">Review Needed</option>
            </select>
          </div>

          <div className="table-card">
            <div className="table-header">
              <h3>Customer Session Table</h3>
              <p>
                Showing {startRow}-{endRow} of {filteredResults.length}
              </p>
            </div>

            <table>
              <thead>
                <tr>
                  <th>Session ID</th>
                  <th>User ID</th>
                  <th>Device</th>
                  <th>Primary Reason</th>
                  <th>Secondary</th>
                  <th>Confidence</th>
                  <th>Level</th>
                  <th>Ground Truth</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>
                {paginatedResults.map((item) => (
                  <tr
                    key={item.session_id}
                    className="clickable-row"
                    onClick={() => {
                      setSelectedSession(item);
                      setSingleResult(item);
                      setSessionSearchId(item.session_id);
                    }}
                  >
                    <td>{item.session_id}</td>
                    <td>{item.user_id}</td>
                    <td>{item.device}</td>
                    <td>{item.predicted_reason}</td>
                    <td>{item.secondary_reason || "-"}</td>
                    <td>{Math.round(item.confidence_score * 100)}%</td>
                    <td>{item.confidence_level}</td>
                    <td>{item.ground_truth_reason || "-"}</td>
                    <td>{item.is_correct ? "✅ Correct" : "⚠ Review"}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="pagination">
              <button
                disabled={currentPage === 1}
                onClick={() => setPage(currentPage - 1)}
              >
                Prev
              </button>

              <span>
                Page {currentPage} of {totalPages}
              </span>

              <button
                disabled={currentPage === totalPages}
                onClick={() => setPage(currentPage + 1)}
              >
                Next
              </button>
            </div>
          </div>
        </>
      )}

      <h2 className="section-title">Single Session Analysis</h2>

      <div className="upload-card session-search-card">
        <input
          type="text"
          placeholder="Paste Session ID or User ID from table"
          value={sessionSearchId}
          onChange={(e) => setSessionSearchId(e.target.value)}
        />

        <button onClick={analyzeSingleSession}>Analyze Session</button>
      </div>

      {singleResult && (
        <div className="single-grid">
          <div className="chart-card">
            <h3>Primary Drop-off Reason</h3>
            <h2 className="reason">{singleResult.predicted_reason}</h2>
            <p className="confidence">
              {Math.round(singleResult.confidence_score * 100)}% Confidence
            </p>
            <p>
              Level: <b>{singleResult.confidence_level}</b>
            </p>
          </div>

          <div className="chart-card">
            <h3>Evidence</h3>
            <ul>
              {singleResult.evidence?.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>

          <div className="chart-card">
            <h3>Recommended Actions</h3>
            <ul>
              {singleResult.recommended_actions?.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {selectedSession && (
        <div className="drawer-overlay" onClick={() => setSelectedSession(null)}>
          <div
            className="session-drawer"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="drawer-header">
              <div>
                <h2>Session Details</h2>
                <p>{selectedSession.session_id}</p>
              </div>

              <button
                className="close-btn"
                onClick={() => setSelectedSession(null)}
              >
                ✕
              </button>
            </div>

            <div className="drawer-summary">
              <div>
                <span>User</span>
                <b>{selectedSession.user_id}</b>
              </div>

              <div>
                <span>Reason</span>
                <b>{formatLabel(selectedSession.predicted_reason)}</b>
              </div>

              <div>
                <span>Confidence</span>
                <b>{Math.round(selectedSession.confidence_score * 100)}%</b>
              </div>

              <div>
                <span>Status</span>
                <b>
                  {selectedSession.is_correct ? "Correct" : "Review Needed"}
                </b>
              </div>
            </div>

            <div className="drawer-section">
              <h3>Evidence</h3>
              <ul>
                {selectedSession.evidence?.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>

            <div className="drawer-section">
              <h3>Recommended Actions</h3>
              <ul>
                {selectedSession.recommended_actions?.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>

            <div className="drawer-section">
              <h3>Signals</h3>
              <div className="pill-grid">
                {Object.entries(selectedSession.signals || {}).map(
                  ([key, value]) => (
                    <span key={key} className={value ? "pill active" : "pill"}>
                      {formatLabel(key)}: {String(value)}
                    </span>
                  )
                )}
              </div>
            </div>

            <div className="drawer-section">
              <h3>Behavior Metrics</h3>
              <div className="metric-grid">
                {Object.entries(selectedSession.behavior_metrics || {}).map(
                  ([key, value]) => (
                    <div key={key} className="metric-item">
                      <span>{formatLabel(key)}</span>
                      <b>{String(value)}</b>
                    </div>
                  )
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [singleFile, setSingleFile] = useState(null);
  const [datasetFile, setDatasetFile] = useState(null);
  const [singleResult, setSingleResult] = useState(null);
  const [datasetResult, setDatasetResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const [searchId, setSearchId] = useState("");
  const [reasonFilter, setReasonFilter] = useState("all");
  const [secondaryFilter, setSecondaryFilter] = useState("all");
  const [confidenceFilter, setConfidenceFilter] = useState("all");
  const [deviceFilter, setDeviceFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");

  const analyzeSession = async () => {
    if (!singleFile) return alert("Please select a JSON file");

    const formData = new FormData();
    formData.append("file", singleFile);

    try {
      setLoading(true);
      const response = await axios.post(
        "http://127.0.0.1:8000/upload-session",
        formData
      );
      setSingleResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Single session analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const analyzeDataset = async () => {
    if (!datasetFile) return alert("Please select a JSONL dataset file");

    const formData = new FormData();
    formData.append("file", datasetFile);

    try {
      setLoading(true);
      const response = await axios.post(
        "http://127.0.0.1:8000/upload-dataset",
        formData
      );
      setDatasetResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Dataset analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const maxValue = (obj) => {
    const values = Object.values(obj || {});
    return values.length ? Math.max(...values) : 1;
  };

  const BarBlock = ({ title, data, colorClass = "" }) => {
    const max = maxValue(data);

    return (
      <div className="card">
        <h2>{title}</h2>

        {Object.entries(data || {}).map(([label, value]) => (
          <div className="bar-row" key={label}>
            <div className="bar-label">{label.replaceAll("_", " ")}</div>

            <div className="bar-track">
              <div
                className={`bar-fill ${colorClass}`}
                style={{ width: `${(value / max) * 100}%` }}
              ></div>
            </div>

            <div className="bar-value">
              {typeof value === "number" && value <= 1
                ? `${Math.round(value * 100)}%`
                : value}
            </div>
          </div>
        ))}
      </div>
    );
  };

  const filteredResults =
    datasetResult?.results?.filter((item) => {
      const search = searchId.toLowerCase();

      const matchesSearch =
        item.session_id?.toLowerCase().includes(search) ||
        item.user_id?.toLowerCase().includes(search);

      const matchesReason =
        reasonFilter === "all" || item.predicted_reason === reasonFilter;

      const matchesSecondary =
        secondaryFilter === "all" || item.secondary_reason === secondaryFilter;

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
        matchesSecondary &&
        matchesConfidence &&
        matchesDevice &&
        matchesStatus
      );
    }) || [];

  const uniqueReasons = Object.keys(datasetResult?.reason_distribution || {});
  const uniqueSecondaryReasons = Object.keys(
    datasetResult?.secondary_reason_distribution || {}
  );
  const uniqueDevices = Object.keys(datasetResult?.device_distribution || {});

  const singleConfidencePercent = singleResult
    ? Math.round(singleResult.confidence_score * 100)
    : "--";

  const correctPercent = datasetResult
    ? (datasetResult.correct_predictions / datasetResult.total_sessions) * 100
    : 0;

  const high = datasetResult?.confidence_distribution?.high || 0;
  const medium = datasetResult?.confidence_distribution?.medium || 0;
  const low = datasetResult?.confidence_distribution?.low || 0;
  const totalConfidence = high + medium + low || 1;

  const highPercent = (high / totalConfidence) * 100;
  const mediumPercent = highPercent + (medium / totalConfidence) * 100;

  return (
    <div className="container">
      <div className="header">
        <h1>DropWise AI</h1>
        <p className="subtitle">
          Customer Drop-off Intelligence Dashboard for Brand Owners
        </p>
      </div>

      <div className="section-title">Dataset Dashboard</div>

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
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Sessions</h3>
              <p>{datasetResult.total_sessions}</p>
            </div>

            <div className="stat-card">
              <h3>Accuracy</h3>
              <p>{datasetResult.accuracy}%</p>
            </div>

            <div className="stat-card">
              <h3>Correct</h3>
              <p>{datasetResult.correct_predictions}</p>
            </div>

            <div className="stat-card">
              <h3>Review Needed</h3>
              <p>{datasetResult.wrong_predictions}</p>
            </div>

            <div className="stat-card">
              <h3>Avg Confidence</h3>
              <p>{Math.round(datasetResult.avg_confidence * 100)}%</p>
            </div>

            <div className="stat-card">
              <h3>Unique Reasons</h3>
              <p>{datasetResult.unique_reasons}</p>
            </div>
          </div>

          <div className="main-grid">
            <BarBlock
              title="Drop-off Reason Distribution"
              data={datasetResult.reason_distribution}
            />

            <BarBlock
              title="Confidence Distribution"
              data={datasetResult.confidence_distribution}
              colorClass="green"
            />

            <div className="card">
              <h2>Prediction Status Split</h2>

              <div className="pie-box">
                <div
                  className="donut"
                  style={{
                    background: `conic-gradient(#16a34a 0 ${correctPercent}%, #f97316 ${correctPercent}% 100%)`,
                  }}
                ></div>

                <div className="legend">
                  <div>🟢 Correct: {datasetResult.correct_predictions}</div>
                  <div>🟠 Review Needed: {datasetResult.wrong_predictions}</div>
                </div>
              </div>
            </div>

            <div className="card">
              <h2>Confidence Split</h2>

              <div className="pie-box">
                <div
                  className="donut"
                  style={{
                    background: `conic-gradient(#2563eb 0 ${highPercent}%, #16a34a ${highPercent}% ${mediumPercent}%, #f97316 ${mediumPercent}% 100%)`,
                  }}
                ></div>

                <div className="legend">
                  <div>🔵 High: {high}</div>
                  <div>🟢 Medium: {medium}</div>
                  <div>🟠 Low: {low}</div>
                </div>
              </div>
            </div>

            <BarBlock
              title="Category-wise Accuracy"
              data={datasetResult.category_accuracy}
              colorClass="purple"
            />

            <BarBlock
              title="Review Count by Reason"
              data={datasetResult.review_count_by_reason}
              colorClass="orange"
            />

            <BarBlock
              title="Average Confidence by Reason"
              data={datasetResult.avg_confidence_by_reason}
              colorClass="green"
            />

            <BarBlock
              title="Secondary Reason Distribution"
              data={datasetResult.secondary_reason_distribution}
              colorClass="orange"
            />

            <BarBlock
              title="Device Distribution"
              data={datasetResult.device_distribution}
              colorClass="purple"
            />
          </div>

          <div className="filters-card">
            <input
              type="text"
              placeholder="Search Session ID or User ID"
              value={searchId}
              onChange={(e) => setSearchId(e.target.value)}
            />

            <select
              value={reasonFilter}
              onChange={(e) => setReasonFilter(e.target.value)}
            >
              <option value="all">All Primary Reasons</option>
              {uniqueReasons.map((reason) => (
                <option key={reason} value={reason}>
                  {reason}
                </option>
              ))}
            </select>

            <select
              value={secondaryFilter}
              onChange={(e) => setSecondaryFilter(e.target.value)}
            >
              <option value="all">All Secondary Reasons</option>
              {uniqueSecondaryReasons.map((reason) => (
                <option key={reason} value={reason}>
                  {reason}
                </option>
              ))}
            </select>

            <select
              value={confidenceFilter}
              onChange={(e) => setConfidenceFilter(e.target.value)}
            >
              <option value="all">All Confidence</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>

            <select
              value={deviceFilter}
              onChange={(e) => setDeviceFilter(e.target.value)}
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
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="all">All Status</option>
              <option value="correct">Correct</option>
              <option value="review">Review Needed</option>
            </select>
          </div>

          <div className="table-card">
            <h2>Customer Session Table</h2>

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
                {filteredResults.map((item) => (
                  <tr key={item.session_id}>
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
          </div>
        </>
      )}

      <div className="section-title">Single Session Analysis</div>

      <div className="upload-card">
        <input
          type="file"
          accept=".json"
          onChange={(e) => setSingleFile(e.target.files[0])}
        />

        <button onClick={analyzeSession}>
          {loading ? "Analyzing..." : "Analyze Single Session"}
        </button>
      </div>

      {singleResult && (
        <div className="main-grid">
          <div className="card">
            <h2>Primary Drop-off Reason</h2>
            <p className="reason">{singleResult.predicted_reason}</p>
            <p className="confidence">{singleConfidencePercent}% Confidence</p>
            <p>
              Level: <b>{singleResult.confidence_level}</b>
            </p>
          </div>

          <div className="card">
            <h2>Signals Detected</h2>

            <div className="signal-grid">
              {Object.entries(singleResult.signals || {})
                .filter(([key]) => key !== "purchase_intent")
                .map(([key, value]) => (
                  <div className="signal" key={key}>
                    {value ? "✅" : "❌"} {key.replaceAll("_", " ")}
                  </div>
                ))}

              <div className="signal intent">
                Purchase Intent: {singleResult.signals?.purchase_intent}
              </div>
            </div>
          </div>

          <div className="card">
            <h2>Evidence</h2>
            <ul>
              {singleResult.evidence?.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </div>

          <div className="card">
            <h2>Recommended Actions</h2>
            <ul>
              {singleResult.recommended_actions?.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
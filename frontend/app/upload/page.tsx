"use client";

import { useState } from "react";

const API_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL ??
  "http://127.0.0.1:8000";

type ProcessingStatus =
  | "idle"
  | "uploading"
  | "extracting"
  | "analyzing"
  | "complete";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);

  const [status, setStatus] =
    useState<ProcessingStatus>("idle");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  function handleFileChange(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const selectedFile =
      event.target.files?.[0] ?? null;

    setFile(selectedFile);
    setStatus("idle");
    setMessage("");
    setError("");
  }

  async function handleUpload() {
    if (!file) {
      return;
    }

    setStatus("uploading");
    setMessage("");
    setError("");

    try {
      // --------------------------------
      // STEP 1 — Upload
      // --------------------------------

      const formData = new FormData();

      formData.append("file", file);

      const uploadResponse = await fetch(
        `${API_URL}/api/v1/reports/users/1/upload`,
        {
          method: "POST",
          body: formData,
        }
      );

      const uploadData = await uploadResponse.json();

      if (!uploadResponse.ok) {
        throw new Error(
          uploadData.detail ??
            `Upload failed with status ${uploadResponse.status}`
        );
      }

      const reportId = uploadData.report_id;

      if (!reportId) {
        throw new Error(
          "Upload succeeded but no report ID was returned."
        );
      }

      // --------------------------------
      // STEP 2 — Extract
      // --------------------------------

      setStatus("extracting");

      const extractResponse = await fetch(
        `${API_URL}/api/v1/reports/${reportId}/extract`,
        {
          method: "POST",
        }
      );

      const extractData =
        await extractResponse.json();

      if (!extractResponse.ok) {
        throw new Error(
          extractData.detail ??
            `Extraction failed with status ${extractResponse.status}`
        );
      }

      // --------------------------------
      // STEP 3 — Analyze
      // --------------------------------

      setStatus("analyzing");

      const analyzeResponse = await fetch(
        `${API_URL}/api/v1/reports/${reportId}/analyze`,
        {
          method: "POST",
        }
      );

      const analyzeData =
        await analyzeResponse.json();

      if (!analyzeResponse.ok) {
        throw new Error(
          analyzeData.detail ??
            `Analysis failed with status ${analyzeResponse.status}`
        );
      }

      // --------------------------------
      // COMPLETE
      // --------------------------------

      setStatus("complete");

      setMessage(
        `Report processed successfully. ${analyzeData.measurements_saved} measurements saved.`
      );

      setFile(null);
    } catch (processingError) {
      setStatus("idle");

      setError(
        processingError instanceof Error
          ? processingError.message
          : "Something went wrong while processing the report."
      );
    }
  }

  const isProcessing =
    status === "uploading" ||
    status === "extracting" ||
    status === "analyzing";

  return (
    <main className="min-h-screen bg-[#080c10] px-6 py-10 text-white lg:px-10">
      <div className="mx-auto max-w-3xl">
        {/* Header */}
        <div>
          <p className="text-xs uppercase tracking-[0.25em] text-cyan-300">
            Health Intelligence
          </p>

          <h1 className="mt-2 text-3xl font-semibold tracking-tight">
            Upload Health Report
          </h1>

          <p className="mt-3 max-w-2xl text-sm leading-6 text-gray-500">
            Add a health report to extract measurements and
            update your personal health timeline.
          </p>
        </div>

        {/* Upload Card */}
        <div className="mt-8 rounded-3xl border border-white/10 bg-[#10161d] p-8">
          <label
            htmlFor="health-report"
            className={`flex flex-col items-center justify-center rounded-2xl border border-dashed border-cyan-400/20 bg-cyan-400/[0.03] px-6 py-16 text-center transition ${
              isProcessing
                ? "cursor-not-allowed opacity-50"
                : "cursor-pointer hover:border-cyan-400/40 hover:bg-cyan-400/[0.05]"
            }`}
          >
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-cyan-400/10 text-2xl text-cyan-300">
              ↑
            </div>

            <h2 className="mt-5 text-lg font-medium">
              Select your health report
            </h2>

            <p className="mt-2 text-sm text-gray-500">
              PDF, TXT or CSV
            </p>

            <span className="mt-5 rounded-xl bg-cyan-400 px-5 py-3 text-sm font-medium text-black">
              Choose File
            </span>

            <input
              id="health-report"
              type="file"
              accept=".pdf,.txt,.csv"
              className="hidden"
              disabled={isProcessing}
              onChange={handleFileChange}
            />
          </label>

          {/* Selected file */}
          {file && !isProcessing && (
            <div className="mt-5 rounded-xl border border-white/10 bg-white/[0.02] p-4">
              <p className="text-xs uppercase tracking-wider text-gray-500">
                Selected Report
              </p>

              <div className="mt-2 flex items-center justify-between gap-4">
                <p className="truncate text-sm text-white">
                  {file.name}
                </p>

                <p className="shrink-0 text-xs text-gray-500">
                  {(file.size / 1024).toFixed(1)} KB
                </p>
              </div>
            </div>
          )}

          {/* Processing status */}
          {isProcessing && (
            <div className="mt-5 rounded-xl border border-cyan-400/20 bg-cyan-400/[0.04] p-4">
              <p className="text-xs uppercase tracking-wider text-cyan-300">
                Processing Report
              </p>

              <div className="mt-4 space-y-3">
                <div className="flex items-center gap-3">
                  <span
                    className={`h-2 w-2 rounded-full ${
                      status === "uploading"
                        ? "animate-pulse bg-cyan-300"
                        : "bg-cyan-400"
                    }`}
                  />

                  <span className="text-sm text-gray-300">
                    Upload report
                  </span>
                </div>

                <div className="flex items-center gap-3">
                  <span
                    className={`h-2 w-2 rounded-full ${
                      status === "extracting"
                        ? "animate-pulse bg-cyan-300"
                        : status === "analyzing"
                          ? "bg-cyan-400"
                          : "bg-gray-700"
                    }`}
                  />

                  <span className="text-sm text-gray-300">
                    Extract report data
                  </span>
                </div>

                <div className="flex items-center gap-3">
                  <span
                    className={`h-2 w-2 rounded-full ${
                      status === "analyzing"
                        ? "animate-pulse bg-cyan-300"
                        : "bg-gray-700"
                    }`}
                  />

                  <span className="text-sm text-gray-300">
                    Analyze health measurements
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Upload button */}
          <button
            type="button"
            disabled={!file || isProcessing}
            onClick={handleUpload}
            className="mt-6 w-full rounded-xl bg-cyan-400 px-5 py-3 text-sm font-medium text-black transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-30"
          >
            {status === "uploading"
              ? "Uploading..."
              : status === "extracting"
                ? "Extracting..."
                : status === "analyzing"
                  ? "Analyzing..."
                  : "Upload Report"}
          </button>

          {/* Success */}
          {message && (
            <div className="mt-4 rounded-xl border border-cyan-400/20 bg-cyan-400/5 px-4 py-3 text-sm text-cyan-300">
              {message}
            </div>
          )}

          {/* Error */}
          {error && (
            <div className="mt-4 rounded-xl border border-red-400/20 bg-red-400/5 px-4 py-3 text-sm text-red-300">
              {error}
            </div>
          )}
        </div>

        {/* Safety note */}
        <p className="mt-5 text-center text-xs leading-5 text-gray-600">
          Reports are processed for health information and
          decision-support purposes. This system does not provide
          medical diagnosis or treatment.
        </p>
      </div>
    </main>
  );
}
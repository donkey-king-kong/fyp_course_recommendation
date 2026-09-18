import { useEffect, useMemo, useState } from 'react'
import {
  fetchAdminBenchmarkCase,
  fetchAdminBenchmarkSummary,
  saveAdminBenchmarkReviews,
} from '../api/adminApi'
import type {
  AdminAnnotatedRecommendation,
  AdminBenchmarkCaseDetailResponse,
  AdminBenchmarkCaseReviewItem,
  AdminBenchmarkCaseSummary,
  AdminBenchmarkReviewStatus,
  AdminBenchmarkSummaryResponse,
  AdminReviewedCandidate,
} from '../types/admin'
import './AdminDashboard.css'

interface AdminDashboardProps {
  adminToken: string
  onAdminLogout: () => void
}

function formatMetric(value: number | null | undefined) {
  if (typeof value !== 'number' || Number.isNaN(value)) {
    return 'N/A'
  }

  return value.toFixed(3)
}

function formatScore(value: number | null | undefined) {
  if (typeof value !== 'number' || Number.isNaN(value)) {
    return 'N/A'
  }

  return value.toFixed(0)
}

function formatLabel(label: string) {
  return label.replaceAll('-', ' ')
}

function scoreBreakdownRows(recommendation: AdminAnnotatedRecommendation) {
  return Object.entries(recommendation.scoreBreakdown)
    .filter(([, value]) => typeof value === 'number')
    .map(([key, value]) => [key, value as number] as const)
}

function getEffectiveReviewStatus(
  benchmarkCase: AdminBenchmarkCaseSummary,
  pendingReviews: Record<string, AdminBenchmarkCaseReviewItem>,
) {
  return pendingReviews[benchmarkCase.caseId]?.adminReviewStatus ?? benchmarkCase.adminReviewStatus
}

function AdminDashboard({ adminToken, onAdminLogout }: AdminDashboardProps) {
  const [summary, setSummary] = useState<AdminBenchmarkSummaryResponse | null>(null)
  const [selectedCaseId, setSelectedCaseId] = useState('')
  const [caseDetail, setCaseDetail] = useState<AdminBenchmarkCaseDetailResponse | null>(null)
  const [pendingReviews, setPendingReviews] = useState<Record<string, AdminBenchmarkCaseReviewItem>>({})
  const [isLoadingSummary, setIsLoadingSummary] = useState(true)
  const [isLoadingCase, setIsLoadingCase] = useState(false)
  const [isSavingReviews, setIsSavingReviews] = useState(false)
  const [error, setError] = useState('')
  const [saveMessage, setSaveMessage] = useState('')

  useEffect(() => {
    let shouldIgnoreResult = false

    async function loadSummary() {
      try {
        setIsLoadingSummary(true)
        setError('')
        const result = await fetchAdminBenchmarkSummary(adminToken)

        if (!shouldIgnoreResult) {
          setSummary(result)
          setSelectedCaseId(result.cases[0]?.caseId ?? '')
        }
      } catch {
        if (!shouldIgnoreResult) {
          setError('Could not load the benchmark dashboard. Log in again or check the backend.')
        }
      } finally {
        if (!shouldIgnoreResult) {
          setIsLoadingSummary(false)
        }
      }
    }

    void loadSummary()

    return () => {
      shouldIgnoreResult = true
    }
  }, [adminToken])

  useEffect(() => {
    if (!selectedCaseId) {
      setCaseDetail(null)
      return
    }

    let shouldIgnoreResult = false

    async function loadCaseDetail() {
      try {
        setIsLoadingCase(true)
        setError('')
        const result = await fetchAdminBenchmarkCase(adminToken, selectedCaseId)

        if (!shouldIgnoreResult) {
          setCaseDetail(result)
        }
      } catch {
        if (!shouldIgnoreResult) {
          setCaseDetail(null)
          setError('Could not load this benchmark case.')
        }
      } finally {
        if (!shouldIgnoreResult) {
          setIsLoadingCase(false)
        }
      }
    }

    void loadCaseDetail()

    return () => {
      shouldIgnoreResult = true
    }
  }, [adminToken, selectedCaseId])

  const selectedCase = useMemo(
    () => summary?.cases.find((item) => item.caseId === selectedCaseId) ?? null,
    [selectedCaseId, summary],
  )
  const weakCaseCount = summary?.cases.filter((item) => item.status !== 'ok').length ?? 0
  const pendingReviewItems = Object.values(pendingReviews)
  const reviewedCaseCount = summary?.cases.filter(
    (item) => getEffectiveReviewStatus(item, pendingReviews) !== 'unreviewed',
  ).length ?? 0

  function updatePendingReview(
    caseId: string,
    adminReviewStatus: AdminBenchmarkReviewStatus,
    adminReviewNotes?: string,
  ) {
    setSaveMessage('')
    setPendingReviews((currentReviews) => ({
      ...currentReviews,
      [caseId]: {
        caseId,
        adminReviewStatus,
        adminReviewNotes: adminReviewNotes ?? currentReviews[caseId]?.adminReviewNotes ?? null,
      },
    }))
  }

  function updatePendingReviewNote(caseId: string, adminReviewNotes: string) {
    const currentCase = summary?.cases.find((item) => item.caseId === caseId)
    const currentStatus = pendingReviews[caseId]?.adminReviewStatus ?? currentCase?.adminReviewStatus ?? 'unreviewed'
    updatePendingReview(caseId, currentStatus, adminReviewNotes)
  }

  async function handleSaveReviews() {
    if (pendingReviewItems.length === 0) {
      return
    }

    try {
      setIsSavingReviews(true)
      setError('')
      setSaveMessage('')
      const result = await saveAdminBenchmarkReviews(adminToken, pendingReviewItems)
      setSummary((currentSummary) => (
        currentSummary
          ? {
              ...currentSummary,
              cases: result.cases,
            }
          : currentSummary
      ))
      setPendingReviews({})
      setSaveMessage(`Saved ${result.updatedCaseIds.length} review decision(s).`)
    } catch {
      setError('Could not save benchmark review decisions.')
    } finally {
      setIsSavingReviews(false)
    }
  }

  if (isLoadingSummary) {
    return (
      <section className="admin-dashboard">
        <p className="admin-loading">Loading benchmark dashboard...</p>
      </section>
    )
  }

  if (!summary) {
    return (
      <section className="admin-dashboard admin-dashboard-empty">
        <h2>Admin Dashboard Unavailable</h2>
        <p>{error || 'The benchmark dashboard could not be loaded.'}</p>
        <button type="button" onClick={onAdminLogout}>
          Log out admin
        </button>
      </section>
    )
  }

  return (
    <section className="admin-dashboard">
      <div className="admin-dashboard-header">
        <div>
          <h2>Benchmark Admin Dashboard</h2>
          <p>
            Visual review surface for saved benchmark cases, backend predictions,
            labels, and ranking metrics.
          </p>
        </div>
        <button type="button" onClick={onAdminLogout}>
          Exit admin mode
        </button>
      </div>

      {error && <p className="admin-error">{error}</p>}

      <div className="admin-metric-strip" aria-label="Benchmark metrics">
        <MetricCard label="Cases" value={summary.caseCount.toString()} />
        <MetricCard label="Weak cases" value={weakCaseCount.toString()} />
        <MetricCard label="Reviewed" value={`${reviewedCaseCount}/${summary.caseCount}`} />
        <MetricCard label="Avg nDCG@5" value={formatMetric(summary.averageNdcgAtK)} />
        <MetricCard label="Precision@5" value={formatMetric(summary.averagePrecisionAtK)} />
      </div>

      <div className="admin-review-save-bar">
        <div>
          <strong>{pendingReviewItems.length} pending review change(s)</strong>
          <span>
            Approve cases you accept as good enough. Disapprove cases that need scoring or label review.
          </span>
        </div>
        {saveMessage && <p>{saveMessage}</p>}
        <button
          type="button"
          disabled={pendingReviewItems.length === 0 || isSavingReviews}
          onClick={handleSaveReviews}
        >
          {isSavingReviews ? 'Saving...' : 'Save Review Decisions'}
        </button>
      </div>

      <div className="admin-dashboard-grid">
        <aside className="admin-case-list" aria-label="Benchmark cases">
          <div className="admin-case-list-header">
            <h3>Cases</h3>
            <p>
              Sorted with weak cases first. Saved predictions generated from{' '}
              {summary.predictionApiUrl || 'the backend'}.
            </p>
          </div>

          <div className="admin-case-buttons">
            {summary.cases.map((benchmarkCase) => (
              <CaseButton
                key={benchmarkCase.caseId}
                benchmarkCase={benchmarkCase}
                isSelected={benchmarkCase.caseId === selectedCaseId}
                effectiveReviewStatus={getEffectiveReviewStatus(benchmarkCase, pendingReviews)}
                onSelect={() => setSelectedCaseId(benchmarkCase.caseId)}
              />
            ))}
          </div>
        </aside>

        <article className="admin-case-detail">
          {selectedCase && (
            <CaseOverview
              benchmarkCase={selectedCase}
              caseDetail={caseDetail}
              isLoadingCase={isLoadingCase}
              pendingReview={pendingReviews[selectedCase.caseId]}
              onReviewChange={updatePendingReview}
              onReviewNoteChange={updatePendingReviewNote}
            />
          )}
        </article>
      </div>
    </section>
  )
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="admin-metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  )
}

function CaseButton({
  benchmarkCase,
  isSelected,
  effectiveReviewStatus,
  onSelect,
}: {
  benchmarkCase: AdminBenchmarkCaseSummary
  isSelected: boolean
  effectiveReviewStatus: AdminBenchmarkReviewStatus
  onSelect: () => void
}) {
  return (
    <button
      type="button"
      className={`admin-case-button ${isSelected ? 'selected' : ''}`}
      onClick={onSelect}
    >
      <span className={`admin-status-pill ${benchmarkCase.status}`}>
        {formatLabel(benchmarkCase.status)}
      </span>
      <span className={`admin-review-pill ${effectiveReviewStatus}`}>
        {formatLabel(effectiveReviewStatus)}
      </span>
      <strong>{benchmarkCase.caseId}</strong>
      <span>
        nDCG {formatMetric(benchmarkCase.ndcgAtK)} · {benchmarkCase.recommendationCount} recs
      </span>
    </button>
  )
}

function CaseOverview({
  benchmarkCase,
  caseDetail,
  isLoadingCase,
  pendingReview,
  onReviewChange,
  onReviewNoteChange,
}: {
  benchmarkCase: AdminBenchmarkCaseSummary
  caseDetail: AdminBenchmarkCaseDetailResponse | null
  isLoadingCase: boolean
  pendingReview?: AdminBenchmarkCaseReviewItem
  onReviewChange: (
    caseId: string,
    adminReviewStatus: AdminBenchmarkReviewStatus,
    adminReviewNotes?: string,
  ) => void
  onReviewNoteChange: (caseId: string, adminReviewNotes: string) => void
}) {
  const effectiveReviewStatus = pendingReview?.adminReviewStatus ?? benchmarkCase.adminReviewStatus
  const effectiveReviewNotes = pendingReview?.adminReviewNotes ?? benchmarkCase.adminReviewNotes ?? ''

  return (
    <>
      <div className="admin-detail-header">
        <div>
          <span className={`admin-status-pill ${benchmarkCase.status}`}>
            {formatLabel(benchmarkCase.status)}
          </span>
          <h3>{benchmarkCase.caseId}</h3>
        </div>
        <div className="admin-detail-metrics">
          <span>nDCG {formatMetric(benchmarkCase.ndcgAtK)}</span>
          <span>Precision {formatMetric(benchmarkCase.precisionAtK)}</span>
          <span>Slots {formatMetric(benchmarkCase.slotFillRate)}</span>
        </div>
      </div>

      <p className="admin-case-description">{benchmarkCase.description}</p>

      <div className="admin-case-facts">
        <Fact label="Career" value={benchmarkCase.careerGoal} />
        <Fact label="Faculty" value={benchmarkCase.studentFaculty || 'N/A'} />
        <Fact label="Completed" value={`${benchmarkCase.completedCourseCount} modules`} />
        <Fact label="Choice slots" value={`${benchmarkCase.choiceSlotCount} slots`} />
      </div>

      <div className="admin-tag-row">
        {benchmarkCase.preferredRecommendationTags.map((tag) => (
          <span key={tag}>{tag}</span>
        ))}
      </div>

      <section className="admin-review-panel">
        <div>
          <h4>Admin Review Decision</h4>
          <p>
            Mark whether this case/prediction outcome is acceptable for the benchmark.
            Save writes the decision into the local benchmark JSON.
          </p>
        </div>
        <div className="admin-review-actions">
          <button
            type="button"
            className={effectiveReviewStatus === 'approved' ? 'selected' : ''}
            onClick={() => onReviewChange(benchmarkCase.caseId, 'approved', effectiveReviewNotes)}
          >
            Approve
          </button>
          <button
            type="button"
            className={effectiveReviewStatus === 'disapproved' ? 'selected danger' : 'danger'}
            onClick={() => onReviewChange(benchmarkCase.caseId, 'disapproved', effectiveReviewNotes)}
          >
            Disapprove
          </button>
        </div>
        <label className="admin-review-note">
          Notes
          <textarea
            value={effectiveReviewNotes}
            onChange={(event) => onReviewNoteChange(benchmarkCase.caseId, event.target.value)}
            placeholder="Optional reason, e.g. SC4051 should rank above cloud because it is the direct distributed-systems match."
          />
        </label>
      </section>

      {isLoadingCase && <p className="admin-loading">Loading case detail...</p>}

      {caseDetail && !isLoadingCase && (
        <>
          <section className="admin-panel">
            <h4>Ranked Predictions</h4>
            <div className="admin-recommendation-stack">
              {caseDetail.rankedRecommendations.map((recommendation, index) => (
                <RecommendationRow
                  key={`${recommendation.courseCode}-${recommendation.matchedChoiceSlotId ?? index}`}
                  recommendation={recommendation}
                  rank={index + 1}
                />
              ))}
            </div>
          </section>

          <section className="admin-panel">
            <h4>Reviewed Candidates</h4>
            <div className="admin-reviewed-grid">
              {caseDetail.reviewedCandidates.map((candidate) => (
                <ReviewedCandidateCard key={candidate.courseCode} candidate={candidate} />
              ))}
            </div>
          </section>

          <section className="admin-panel">
            <h4>Case Inputs</h4>
            <div className="admin-input-columns">
              <CodeList title="Completed modules" values={caseDetail.completedCourseCodes} />
              <CodeList
                title="Choice slots"
                values={caseDetail.choiceSlots.map((slot) => String(slot.courseCode))}
              />
            </div>
          </section>
        </>
      )}
    </>
  )
}

function Fact({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  )
}

function RecommendationRow({
  recommendation,
  rank,
}: {
  recommendation: AdminAnnotatedRecommendation
  rank: number
}) {
  const scoreRows = scoreBreakdownRows(recommendation)

  return (
    <details className="admin-recommendation-row" open={rank <= 2}>
      <summary>
        <span className="admin-rank">#{rank}</span>
        <span>
          <strong>{recommendation.courseCode}</strong>
          <small>{recommendation.title}</small>
        </span>
        <span className={`admin-relevance-pill ${recommendation.expectedRelevance}`}>
          {formatLabel(recommendation.expectedRelevance)}
        </span>
        <span className="admin-score">{formatScore(recommendation.score)}</span>
      </summary>

      <div className="admin-recommendation-body">
        <p>{recommendation.reason || 'No explanation returned.'}</p>
        <div className="admin-score-grid">
          {scoreRows.map(([key, value]) => (
            <div key={key}>
              <span>{key}</span>
              <strong>{formatScore(value)}</strong>
            </div>
          ))}
        </div>
        <div className="admin-note-grid">
          <p>
            <strong>Slot:</strong> {recommendation.matchedChoiceSlotId || 'N/A'}
          </p>
          <p>
            <strong>Constraint valid:</strong> {recommendation.constraintValid ? 'yes' : 'no'}
          </p>
          <p>
            <strong>Expected path:</strong> {recommendation.expectedSkillPath || 'Not reviewed'}
          </p>
          <p>
            <strong>Review notes:</strong> {recommendation.reviewNotes || 'No reviewed note.'}
          </p>
        </div>
      </div>
    </details>
  )
}

function ReviewedCandidateCard({ candidate }: { candidate: AdminReviewedCandidate }) {
  return (
    <div className="admin-reviewed-card">
      <div>
        <span className={`admin-relevance-pill ${candidate.expectedRelevance}`}>
          {formatLabel(candidate.expectedRelevance)}
        </span>
        <h5>{candidate.courseCode}</h5>
      </div>
      <p>{candidate.title}</p>
      <p>
        {candidate.wasRecommended
          ? `Predicted rank ${candidate.predictedRank}, score ${formatScore(candidate.predictedScore)}`
          : 'Not returned by saved prediction'}
      </p>
    </div>
  )
}

function CodeList({ title, values }: { title: string; values: string[] }) {
  return (
    <div>
      <h5>{title}</h5>
      <div className="admin-code-list">
        {values.map((value) => (
          <span key={value}>{value}</span>
        ))}
      </div>
    </div>
  )
}

export default AdminDashboard

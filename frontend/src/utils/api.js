export const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';

export async function apiRequest(endpoint, options = {}) {
    const url = `${BASE_URL}${endpoint}`;
    
    if (options.body && !(options.body instanceof FormData)) {
        options.headers = {
            'Content-Type': 'application/json',
            ...(options.headers || {})
        };
    }
    
    const response = await fetch(url, options);
    const data = await response.json();
    
    if (data.status !== 'success') {
        throw new Error(data.message || 'API request failed');
    }
    
    return data;
}

export const loginUser = (email, password) => apiRequest('/api/login', { method: 'POST', body: JSON.stringify({ email, password }) });
export const signupUser = (userData) => apiRequest('/api/signup', { method: 'POST', body: JSON.stringify(userData) });

export const getProfile = (email) => apiRequest(`/api/profile?email=${encodeURIComponent(email)}`);
export const updateProfile = (profileData) => apiRequest('/api/profile', { method: 'POST', body: JSON.stringify(profileData) });

export const uploadResume = (email, file) => {
    const formData = new FormData();
    formData.append('email', email);
    formData.append('resume', file);
    return apiRequest('/api/profile/upload-resume', { method: 'POST', body: formData });
};

export const setDefaultResume = (email, resumeId) => apiRequest('/api/profile/set-default-resume', { method: 'POST', body: JSON.stringify({ email, resume_id: resumeId }) });
export const getResumes = (email) => apiRequest(`/api/profile/resumes?email=${encodeURIComponent(email)}`);

export const getJobs = (recruiterEmail) => recruiterEmail 
    ? apiRequest(`/api/jobs?recruiter_email=${encodeURIComponent(recruiterEmail)}`) 
    : apiRequest('/api/jobs');

export const getJob = (jobId) => apiRequest(`/api/jobs/${encodeURIComponent(jobId)}`);
export const createJob = (jobData) => apiRequest('/api/jobs', { method: 'POST', body: JSON.stringify(jobData) });
export const updateJob = (jobId, jobData) => apiRequest(`/api/jobs/${encodeURIComponent(jobId)}`, { method: 'PUT', body: JSON.stringify(jobData) });
export const deleteJob = (jobId) => apiRequest(`/api/jobs/${encodeURIComponent(jobId)}`, { method: 'DELETE' });

export const applyForJob = (formData) => apiRequest('/api/jobs/apply', { method: 'POST', body: formData });
export const previewScore = (formData) => apiRequest('/api/jobs/preview_score', { method: 'POST', body: formData });

export const getCandidateApplications = (email) => apiRequest(`/api/candidate/applications?email=${encodeURIComponent(email)}`);
export const getCandidateAppliedJobs = (email) => apiRequest(`/api/candidate/applied-jobs?email=${encodeURIComponent(email)}`);

export const getJobApplications = (jobId) => apiRequest(`/api/jobs/${encodeURIComponent(jobId)}/applications`);
export const updateApplicationStatus = (jobId, appId, status) => apiRequest(`/api/jobs/${encodeURIComponent(jobId)}/applications/${encodeURIComponent(appId)}/status`, { method: 'PATCH', body: JSON.stringify({ status }) });
export const bulkUpdateStatus = (jobId, action, threshold, direction) => apiRequest(`/api/jobs/${encodeURIComponent(jobId)}/applications/bulk-status`, { method: 'PATCH', body: JSON.stringify({ action, threshold, direction }) });

export const getRecruiterApplications = (email) => apiRequest(`/api/recruiter/applications?email=${encodeURIComponent(email)}`);

export const generateContent = (prompt, context) => apiRequest('/api/generate-content', { method: 'POST', body: JSON.stringify({ prompt, context }) });
export const generateAssessment = (role) => apiRequest('/api/generate-assessment', { method: 'POST', body: JSON.stringify({ role }) });
export const analyzeResumes = (formData) => apiRequest('/api/analyze', { method: 'POST', body: formData });
export const saveResume = (data) => apiRequest('/api/save-resume', { method: 'POST', body: JSON.stringify(data) });

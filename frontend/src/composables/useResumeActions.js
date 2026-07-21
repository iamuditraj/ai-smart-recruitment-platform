import { uploadResume as uploadResumeApi, setDefaultResume as setDefaultResumeApi, getResumes as getResumesApi } from '../utils/api';

export function useResumeActions(authStore) {
    async function fetchResumes() {
        if (!authStore.user?.value?.email) return;
        try {
            const data = await getResumesApi(authStore.user.value.email);
            if (data.status === 'success') {
                authStore.resumes.value = data.resumes;
            }
        } catch (error) {
            console.error('fetchResumes error:', error);
        }
    }

    async function uploadResume(file) {
        if (!authStore.user?.value?.email) return { success: false, message: 'Not logged in' };
        try {
            const data = await uploadResumeApi(authStore.user.value.email, file);
            if (data.status === 'success') {
                await authStore.refreshUser();
                await fetchResumes();
                return { success: true, url: data.resumeUrl, name: data.resumeName };
            } else {
                return { success: false, message: data.message };
            }
        } catch (error) {
            console.error('Resume upload error:', error);
            return { success: false, message: error.message || 'Server connection failed' };
        }
    }

    async function setDefaultResume(resume_id) {
        if (!authStore.user?.value?.email) return { success: false, message: 'Not logged in' };
        try {
            const data = await setDefaultResumeApi(authStore.user.value.email, resume_id);
            if (data.status === 'success') {
                await authStore.refreshUser();
                await fetchResumes();
                return { success: true };
            } else {
                return { success: false, message: data.message };
            }
        } catch (error) {
            console.error('Set default resume error:', error);
            return { success: false, message: error.message || 'Server connection failed' };
        }
    }

    return {
        fetchResumes,
        uploadResume,
        setDefaultResume
    };
}

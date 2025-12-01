import { useState, useEffect, useRef } from 'react'
import CountUpNumber from '../components/CountUpNumber'
import { useAuth } from '../hooks/useAuth'
import { profileAPI } from '../services/api'
import toast from 'react-hot-toast'
import {
  UserCircleIcon,
  CameraIcon,
  CheckIcon,
  EyeIcon,
  EyeSlashIcon,
  BellIcon,
  EnvelopeIcon,
  MapPinIcon,
  BriefcaseIcon
} from '@heroicons/react/24/outline'

const Profile = () => {
  const { user } = useAuth()
  const fileInputRef = useRef(null)
  
  const [profile, setProfile] = useState({
    name: '',
    email: '',
    location: '',
    role: 'professional',
    tagline: '',
    avatar: null,
    stats: { total_goals: 0, completed_goals: 0, streak_days: 0 },
    preferences: { email_notifications: true, weekly_summary: true, focus_areas: [] }
  })
  
  const [loading, setLoading] = useState({ profile: false, preferences: false, password: false, avatar: false })
  const [showPassword, setShowPassword] = useState({ current: false, new: false, confirm: false })
  const [passwords, setPasswords] = useState({ current: '', new: '', confirm: '' })
  const [editMode, setEditMode] = useState({ profile: false, preferences: false })

  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      const data = await profileAPI.getProfile()
      setProfile(data)
    } catch (error) {
      console.error('Profile fetch error:', error)
      // Set default profile data if fetch fails
      setProfile({
        name: 'Demo User',
        email: 'demo@gmail.com',
        location: '',
        role: 'professional',
        tagline: 'AI-powered life goals explorer',
        avatar: null,
        stats: { total_goals: 12, completed_goals: 8, streak_days: 15 },
        preferences: { email_notifications: true, weekly_summary: true, focus_areas: ['career', 'wellness'] }
      })
    }
  }

  const handleProfileSave = async () => {
    setLoading(prev => ({ ...prev, profile: true }))
    try {
      await profileAPI.updateProfile({
        name: profile.name,
        email: profile.email,
        location: profile.location,
        role: profile.role,
        tagline: profile.tagline
      })
      setEditMode(prev => ({ ...prev, profile: false }))
      toast.success('Profile updated successfully')
    } catch (error) {
      toast.error('Failed to update profile')
    } finally {
      setLoading(prev => ({ ...prev, profile: false }))
    }
  }

  const handlePreferencesSave = async () => {
    setLoading(prev => ({ ...prev, preferences: true }))
    try {
      await profileAPI.updatePreferences(profile.preferences)
      setEditMode(prev => ({ ...prev, preferences: false }))
      toast.success('Preferences updated successfully')
    } catch (error) {
      toast.error('Failed to update preferences')
    } finally {
      setLoading(prev => ({ ...prev, preferences: false }))
    }
  }

  const handlePasswordChange = async () => {
    if (passwords.new !== passwords.confirm) {
      toast.error('New passwords do not match')
      return
    }
    if (passwords.new.length < 6) {
      toast.error('Password must be at least 6 characters')
      return
    }

    setLoading(prev => ({ ...prev, password: true }))
    try {
      await profileAPI.changePassword({
        current_password: passwords.current,
        new_password: passwords.new
      })
      setPasswords({ current: '', new: '', confirm: '' })
      toast.success('Password changed successfully')
    } catch (error) {
      toast.error('Failed to change password')
    } finally {
      setLoading(prev => ({ ...prev, password: false }))
    }
  }

  const handleAvatarUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    if (!file.type.startsWith('image/')) {
      toast.error('Please select an image file')
      return
    }

    if (file.size > 5 * 1024 * 1024) {
      toast.error('File size must be less than 5MB')
      return
    }

    setLoading(prev => ({ ...prev, avatar: true }))
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      // Create preview URL for immediate display
      const previewUrl = URL.createObjectURL(file)
      setProfile(prev => ({ ...prev, avatar: previewUrl }))
      
      await profileAPI.uploadAvatar(formData)
      toast.success('Avatar updated successfully')
    } catch (error) {
      console.error('Avatar upload error:', error)
      const errorMessage = error.response?.data?.detail || 'Failed to upload avatar'
      toast.error(errorMessage)
      // Reset file input
      if (event.target) event.target.value = ''
    } finally {
      setLoading(prev => ({ ...prev, avatar: false }))
    }
  }

  const toggleFocusArea = (area) => {
    setProfile(prev => ({
      ...prev,
      preferences: {
        ...prev.preferences,
        focus_areas: prev.preferences.focus_areas.includes(area)
          ? prev.preferences.focus_areas.filter(a => a !== area)
          : [...prev.preferences.focus_areas, area]
      }
    }))
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Hero Identity Card */}
        <div className="backdrop-blur-sm bg-white/70 rounded-3xl p-8 shadow-xl border border-white/20 mb-8">
            <div className="flex flex-col md:flex-row items-center gap-8">
              <div className="relative">
                {profile.avatar ? (
                  <img
                    src={profile.avatar}
                    alt="Profile"
                    className="w-32 h-32 rounded-full object-cover border-4 border-white shadow-lg"
                  />
                ) : (
                  <div className="w-32 h-32 rounded-full bg-gradient-to-r from-purple-100 to-pink-100 border-4 border-white shadow-lg flex items-center justify-center">
                    <UserCircleIcon className="w-20 h-20 text-purple-400" />
                  </div>
                )}
                <button
                  onClick={() => fileInputRef.current?.click()}
                  disabled={loading.avatar}
                  className="absolute bottom-0 right-0 bg-purple-600 text-white p-2 rounded-full hover:bg-purple-700 transition-colors shadow-lg"
                >
                  {loading.avatar ? (
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  ) : (
                    <CameraIcon className="w-5 h-5" />
                  )}
                </button>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleAvatarUpload}
                  className="hidden"
                />
              </div>
              
              <div className="flex-1 text-center md:text-left">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">{profile.name}</h1>
                <p className="text-purple-600 font-medium mb-2">{profile.email}</p>
                <p className="text-gray-600 mb-6">{profile.tagline}</p>
                
                <div className="grid grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-900">
                      <CountUpNumber endValue={profile.stats.total_goals} />
                    </div>
                    <div className="text-sm text-gray-600">Total Goals</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      <CountUpNumber endValue={profile.stats.completed_goals} />
                    </div>
                    <div className="text-sm text-gray-600">Completed</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">
                      <CountUpNumber endValue={profile.stats.streak_days} />
                    </div>
                    <div className="text-sm text-gray-600">Day Streak</div>
                  </div>
                </div>
              </div>
            </div>
        </div>

        {/* Personal Info */}
        <div className="backdrop-blur-sm bg-white/70 rounded-3xl p-8 shadow-xl border border-white/20 mb-8 hover:shadow-2xl transition-all duration-300">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Personal Information</h2>
              <button
                onClick={() => editMode.profile ? handleProfileSave() : setEditMode(prev => ({ ...prev, profile: true }))}
                disabled={loading.profile}
                className="px-4 py-2 bg-purple-600 text-white rounded-xl hover:bg-purple-700 transition-colors disabled:opacity-50"
              >
                {loading.profile ? (
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Saving...
                  </div>
                ) : editMode.profile ? (
                  <div className="flex items-center gap-2">
                    <CheckIcon className="w-4 h-4" />
                    Save
                  </div>
                ) : (
                  'Edit'
                )}
              </button>
            </div>
            
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
                <input
                  type="text"
                  value={profile.name}
                  onChange={(e) => setProfile(prev => ({ ...prev, name: e.target.value }))}
                  disabled={!editMode.profile}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:bg-gray-50"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                <input
                  type="email"
                  value={profile.email}
                  onChange={(e) => setProfile(prev => ({ ...prev, email: e.target.value }))}
                  disabled={!editMode.profile}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:bg-gray-50"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
                <input
                  type="text"
                  value={profile.location}
                  onChange={(e) => setProfile(prev => ({ ...prev, location: e.target.value }))}
                  disabled={!editMode.profile}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:bg-gray-50"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Role</label>
                <select
                  value={profile.role}
                  onChange={(e) => setProfile(prev => ({ ...prev, role: e.target.value }))}
                  disabled={!editMode.profile}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:bg-gray-50"
                >
                  <option value="student">Student</option>
                  <option value="professional">Professional</option>
                  <option value="creator">Creator</option>
                </select>
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">Tagline</label>
                <input
                  type="text"
                  value={profile.tagline}
                  onChange={(e) => setProfile(prev => ({ ...prev, tagline: e.target.value }))}
                  disabled={!editMode.profile}
                  placeholder="AI-powered life goals explorer"
                  className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:bg-gray-50"
                />
              </div>
            </div>
        </div>

        {/* Preferences */}
        <div className="backdrop-blur-sm bg-white/70 rounded-3xl p-8 shadow-xl border border-white/20 mb-8 hover:shadow-2xl transition-all duration-300">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Preferences</h2>
              <button
                onClick={() => editMode.preferences ? handlePreferencesSave() : setEditMode(prev => ({ ...prev, preferences: true }))}
                disabled={loading.preferences}
                className="px-4 py-2 bg-purple-600 text-white rounded-xl hover:bg-purple-700 transition-colors disabled:opacity-50"
              >
                {loading.preferences ? (
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Saving...
                  </div>
                ) : editMode.preferences ? (
                  <div className="flex items-center gap-2">
                    <CheckIcon className="w-4 h-4" />
                    Save
                  </div>
                ) : (
                  'Edit'
                )}
              </button>
            </div>
            
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-medium text-gray-900">Email Notifications</h3>
                  <p className="text-sm text-gray-600">Receive updates about your goals</p>
                </div>
                <button
                  onClick={() => setProfile(prev => ({
                    ...prev,
                    preferences: { ...prev.preferences, email_notifications: !prev.preferences.email_notifications }
                  }))}
                  disabled={!editMode.preferences}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    profile.preferences.email_notifications ? 'bg-purple-600' : 'bg-gray-200'
                  } disabled:opacity-50`}
                >
                  <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                    profile.preferences.email_notifications ? 'translate-x-6' : 'translate-x-1'
                  }`} />
                </button>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-medium text-gray-900">Weekly Summary</h3>
                  <p className="text-sm text-gray-600">Get weekly progress reports</p>
                </div>
                <button
                  onClick={() => setProfile(prev => ({
                    ...prev,
                    preferences: { ...prev.preferences, weekly_summary: !prev.preferences.weekly_summary }
                  }))}
                  disabled={!editMode.preferences}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    profile.preferences.weekly_summary ? 'bg-purple-600' : 'bg-gray-200'
                  } disabled:opacity-50`}
                >
                  <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                    profile.preferences.weekly_summary ? 'translate-x-6' : 'translate-x-1'
                  }`} />
                </button>
              </div>
              
              <div>
                <h3 className="font-medium text-gray-900 mb-3">Focus Areas</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {['career', 'finance', 'wellness', 'learning'].map((area) => (
                    <button
                      key={area}
                      onClick={() => toggleFocusArea(area)}
                      disabled={!editMode.preferences}
                      className={`p-3 rounded-xl border-2 transition-all capitalize ${
                        profile.preferences.focus_areas.includes(area)
                          ? 'border-purple-600 bg-purple-50 text-purple-700'
                          : 'border-gray-200 bg-white text-gray-600 hover:border-purple-300'
                      } disabled:opacity-50`}
                    >
                      {area}
                    </button>
                  ))}
                </div>
              </div>
            </div>
        </div>

        {/* Security */}
        <div className="backdrop-blur-sm bg-white/70 rounded-3xl p-8 shadow-xl border border-white/20 hover:shadow-2xl transition-all duration-300">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Security</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Current Password</label>
                <div className="relative">
                  <input
                    type={showPassword.current ? 'text' : 'password'}
                    value={passwords.current}
                    onChange={(e) => setPasswords(prev => ({ ...prev, current: e.target.value }))}
                    className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 pr-12"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(prev => ({ ...prev, current: !prev.current }))}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    {showPassword.current ? <EyeSlashIcon className="w-5 h-5" /> : <EyeIcon className="w-5 h-5" />}
                  </button>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">New Password</label>
                <div className="relative">
                  <input
                    type={showPassword.new ? 'text' : 'password'}
                    value={passwords.new}
                    onChange={(e) => setPasswords(prev => ({ ...prev, new: e.target.value }))}
                    className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 pr-12"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(prev => ({ ...prev, new: !prev.new }))}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    {showPassword.new ? <EyeSlashIcon className="w-5 h-5" /> : <EyeIcon className="w-5 h-5" />}
                  </button>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Confirm New Password</label>
                <div className="relative">
                  <input
                    type={showPassword.confirm ? 'text' : 'password'}
                    value={passwords.confirm}
                    onChange={(e) => setPasswords(prev => ({ ...prev, confirm: e.target.value }))}
                    className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 pr-12"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(prev => ({ ...prev, confirm: !prev.confirm }))}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    {showPassword.confirm ? <EyeSlashIcon className="w-5 h-5" /> : <EyeIcon className="w-5 h-5" />}
                  </button>
                </div>
              </div>
              
              <button
                onClick={handlePasswordChange}
                disabled={loading.password || !passwords.current || !passwords.new || !passwords.confirm}
                className="px-6 py-3 bg-purple-600 text-white rounded-xl hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading.password ? (
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Changing Password...
                  </div>
                ) : (
                  'Change Password'
                )}
              </button>
            </div>
        </div>

      </div>
    </div>
  )
}

export default Profile
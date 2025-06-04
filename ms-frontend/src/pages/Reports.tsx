import Navbar from '../components/Navbar'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../Auth/AuthContext'
import Reports from '../components/Reports';

const Dashboard = () => {
  const { isAuthenticated, keycloak } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/" replace />
  }

  if (!keycloak.authenticated) {
    return <Navigate to="/" replace />
  }

  return (
    <>
      <Navbar />
      <Reports />
    </>
  )
}

export default Dashboard

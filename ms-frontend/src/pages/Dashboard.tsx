import Navbar from '../components/Navbar'
import CDRTable from '../components/CDRTable'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../Auth/AuthContext'

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
      <CDRTable />
    </>
  )
}

export default Dashboard

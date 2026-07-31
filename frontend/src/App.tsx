import { useQuery } from '@tanstack/react-query'
import { Alert, Box, Button, Card, CardContent, CircularProgress } from '@mui/material'
import './App.css'

async function fetchHealth() {
  const response = await fetch('http://localhost:8000/health')

  if (!response.ok) {
    throw new Error('Failed to reach the backend health endpoint')
  }

  return response.json() as Promise<{ status: string; message: string }>
}

function App() {
  const { data, error, isFetching, refetch } = useQuery({
    queryKey: ['health'],
    queryFn: fetchHealth,
    enabled: false,
  })

  return (
    <Box className="app-shell">
      <Box className="content-card">
        <h1>Frontend ↔ Backend</h1>
        <p className="subtitle">
          Click the button to send a request to the FastAPI health endpoint and display the response.
        </p>

        <Button
          variant="contained"
          size="large"
          onClick={() => void refetch()}
          disabled={isFetching}
        >
          {isFetching ? <CircularProgress size={20} color="inherit" /> : 'Call /health'}
        </Button>

        {error ? (
          <Alert severity="error">{error.message}</Alert>
        ) : null}

        {data ? (
          <Card variant="outlined" className="response-card">
            <CardContent>
              <p className="card-label">Response from FastAPI</p>
              <h2>Status: {data.status}</h2>
              <p>{data.message}</p>
            </CardContent>
          </Card>
        ) : null}
      </Box>
    </Box>
  )
}

export default App

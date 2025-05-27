import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import {RouterProvider,createBrowserRouter} from 'react-router-dom'
import CreateTrip from './components/custom/Create_trip.jsx'
import Header from './components/custom/Header.jsx'
import Chatbot from './components/custom/Chatbot.jsx'
import Features from './components/custom/Features.jsx'
import Form from './components/custom/Form.jsx'
import Login from './components/custom/Login'
import SignUp from './components/custom/SignUp'
import Finetune from './components/custom/Finetune.jsx'
import Itinerary from './components/custom/Itinerary.jsx'

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />
  },
  {
    path: '/create-trip',
    element: <CreateTrip />
  },
  {
    path: '/feature',
    element: <Features />
  },
  {
    path: '/form',
    element: <Form />
  },
  {
    path: '/login',
    element: <Login />
  },
  {
    path: '/signup',
    element: <SignUp />
  },
  {
    path: '/finetune',
    element: <Finetune />
  },
  {
    path: '/iterary',
    element: < Itinerary/>
  }
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Header />
    <RouterProvider router={router}/>
    <Chatbot />
  </StrictMode>
)

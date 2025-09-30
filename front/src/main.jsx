import { BrowserRouter } from "react-router-dom"
import { createRoot } from 'react-dom/client'
import './index.css'
import Layout from './Layout.jsx'

createRoot(document.getElementById('root')).render(
  <BrowserRouter>

    <Layout />
  </BrowserRouter>

)

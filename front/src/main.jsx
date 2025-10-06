import { BrowserRouter } from "react-router-dom"
import { createRoot } from 'react-dom/client'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min'
import 'bootstrap-icons/font/bootstrap-icons.min.css'
import '@fortawesome/fontawesome-free/css/all.min.css'
import './index.css'
import { Layout } from "./Layout"


createRoot(document.getElementById('root')).render(
  <BrowserRouter>

    <Layout />
  </BrowserRouter>

)

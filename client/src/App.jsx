import { Routes, Route } from 'react-router-dom'
import NotFound from './pages/NotFoundPage'
import SplashPage from './pages/SplashPage'
import EncodePage from './pages/EncodePage'
import DecodePage from './pages/DecodePage'
import AnalyzePage from './pages/AnalyzePage'

/**
 * Defines and provides which page to load based on current route
 * @returns Render of pages for respective routes
 */
export default function App() {

    return (
        <div className="bg-dark d-flex vh-100">
            {/* Container that defines all of the routes available on the website */}
            <Routes>
            
                {/* Pages that don't require authentication to access */}
                <Route path='/' element={<SplashPage />} />
                <Route path='/encode' element={<EncodePage />} />
                <Route path='/decode' element={<DecodePage />} />
                <Route path='/analyze' element={<AnalyzePage />} />
                <Route path='/*' element={<NotFound />} />
            
            </Routes>
        </div>
    );

};
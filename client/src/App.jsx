import { Routes, Route } from 'react-router-dom'
import NotFound from './pages/NotFoundPage'
import SplashPage from './pages/SplashPage'
import EncodePage from './pages/EncodePage'
import EncodeImage from './pages/EncodeImage'
import DecodePage from './pages/DecodePage'

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
                <Route path='/encode1' element={<DecodePage />} />
                <Route path='/encode' element={<EncodePage />} />
                <Route path='/encode/image' element={<EncodeImage />} />
                <Route path='/decode' element={<DecodePage />} />
                <Route path='/*' element={<NotFound />} />
            
            </Routes>
        </div>
    );

};
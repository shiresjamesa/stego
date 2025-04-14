import { useNavigate } from 'react-router-dom';
import Logo from '../components/objects/Logo';

/**
 * Renders the splash page form component, navigates to encode and deocde forms
 * @returns Render of splash page form
 */
export default function SplashPage() {

    // Initialize page navigation
    const navigate = useNavigate();

    // Navigates to encode page on encode button click
    const handleEncodeButton = () => {
        navigate('/encode');
    };

    // Navigates to decode page on decode button click
    const handleDecodeButton = () => {
        navigate('/decode');
    };

    // Navigates to decode page on decode button click
    const handleAnalyzeButton = () => {
        navigate('/analyze');
    };

    // Render components of splash page form
    return (
        <>
            {/* Container which holds all components in form */}
            <div className="container splashpage-form-container pt-5 px-5 bg-light">

                {/* Row containing logo */}
                <div className="row">
                    <Logo />
                </div>

                {/* Row containing Encode and Decode buttons */}
                <div className="row pt-5 pb-5 justify-content-evenly">

                    {/* Encode button */}
                    <div className="col-4 d-grid">
                        <button 
                            type="button" 
                            className="btn btn-primary"
                            onClick={ handleEncodeButton }>
                            Encode
                        </button>
                    </div>
                    
                    {/* Decode button */}
                    <div className="col-4 d-grid">
                        <button 
                            type="button" 
                            className="btn btn-primary"
                            onClick={ handleDecodeButton }>
                            Decode
                        </button>
                    </div>


                    {/* Decode button */}
                    <div className="col-4 d-grid">
                        <button 
                            type="button" 
                            className="btn btn-primary"
                            onClick={ handleAnalyzeButton }>
                            Analyze
                        </button>
                    </div>

                </div>
            </div>
        </>
    );
    
};
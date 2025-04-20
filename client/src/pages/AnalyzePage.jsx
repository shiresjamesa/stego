import { useNavigate, useOutletContext } from 'react-router-dom';
import { useState } from 'react';
import axios from '../api/axios';
import ByteFrequencyChart from '../components/ByteFrequencyChart';

/**
 * Renders analyze page and provides functionality
 * @returns Render of analyze page
 */
export default function AnalyzePage() {

    const navigate = useNavigate();
    const [file1, setFile1] = useState(null);
    const [file2, setFile2] = useState(null);
    const [preview1, setPreview1] = useState(null);
    const [preview2, setPreview2] = useState(null);
    const [analysis1, setAnalysis1] = useState(null);
    const [analysis2, setAnalysis2] = useState(null);
    const [loading, setLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState(' ');

    // Navigates to splashpage on Return button click
    const handleReturnClick = () => {
        navigate("/")
    };

    const handleFile1Change = async (e) => {
        e.preventDefault();
        const selectedFile = e.target.files[0];
        if (!selectedFile) return;
    
        const fileType = selectedFile.type;
        if (fileType === "image/png" || fileType === "image/jpeg") {
            setFile1(selectedFile);
            const objectUrl = URL.createObjectURL(selectedFile);
            setPreview1(objectUrl);
            await analyzeImage(selectedFile, setAnalysis1);
        }
    };
    
    const handleFile2Change = async (e) => {
        const selectedFile = e.target.files[0];
        if (!selectedFile) return;
    
        const fileType = selectedFile.type;
        if (fileType === "image/png" || fileType === "image/jpeg") {
            setFile2(selectedFile);
            const objectUrl = URL.createObjectURL(selectedFile);
            setPreview2(objectUrl);
            await analyzeImage(selectedFile, setAnalysis2);
        }
    };

    const analyzeImage = async (file, setAnalysis) => {
        
        const formData = new FormData();
        formData.append('file', file);
    
        try {
            const response = await axios.post('/analyze/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            const { entropy, byteFreq } = response.data

            console.log(entropy)
            console.log(byteFreq)
            setAnalysis(response.data);
        } catch (error) {
            console.error("Analysis failed:", error);
            setAnalysis({ error: "Failed to analyze image." });
        }
    };

    const handleReset = async (e) => {
        setAnalysis1(null)
        setAnalysis2(null)
        setFile1(null)
        setFile2(null)
    }
 
    // Render components of the analyze page
    return (
        <>
            {/* Container which holds all components in form */}
            <div className="container encode-page-container bg-light px-4 pt-2">

                {/* Row containing page title */}
                <div className="row pt-3 text-center">
                    <h4>Analyze</h4>
                </div>
                
                <br />

                {/* Row containing file input, text input, and output */}
                <div className="row justify-content-center">

                    {/* LEFT SIDE: Image 1 */}

                        {/* File upload window */}
                        {!analysis1 && (
                            <div className="col-5 pt-2 image-analysis-form" style={{ alignItems: 'center', justifyContent: 'center'}}>
                                <div className="row">
                                    <div className="form-group text-center">
                                        <label htmlFor="fileUpload" className="form-label">Upload Original Media:</label>
                                        <input 
                                            type="file" 
                                            className="form-control" 
                                            id="fileUpload" 
                                            onChange={ handleFile1Change } 
                                            accept=".png, .jpg, .jpeg"
                                            style={{
                                                padding: '10px', 
                                                border: '2px dashed #007bff',
                                                cursor: 'pointer'
                                            }}
                                        />
                                    </div>
                                </div>
                            </div>
                        )}
                            
                        
                        {/* Analysis window */}
                        {analysis1 && (
                            <div className="col-5 pt-2 image-analysis-form">
                                {/* Row for entropy */}
                                <div className="row">
                                    <div className="d-flex justify-content-center">
                                        <h5><strong>Entropy:</strong> {analysis1.entropy?.toFixed(4)}</h5>
                                    </div>
                                </div>
                                    
                                {/* Row for viewport */}
                                <div className="row">

                                </div>


                                {/* Row for byte graph */}
                                <div className="row">
                                    <div className="mt-3 p-3 bg-white border rounded shadow-sm">
                                        <ByteFrequencyChart byteCounts={analysis1.byte_counts} />
                                    </div>
                                </div>
                                

                            </div>
                            
                            
                        )}
                    
                        <div className="col-1" />

                        {/* File upload window */}
                        {!analysis2 && (
                            <div className="col-5 pt-2 image-analysis-form" style={{ alignItems: 'center', justifyContent: 'center'}}>
                                <div className="row">
                                    <div className="form-group text-center">
                                        <label htmlFor="fileUpload" className="form-label">Upload Original Media:</label>
                                        <input 
                                            type="file" 
                                            className="form-control" 
                                            id="fileUpload" 
                                            onChange={ handleFile2Change } 
                                            accept=".png, .jpg, .jpeg"
                                            style={{
                                                padding: '10px', 
                                                border: '2px dashed #007bff',
                                                cursor: 'pointer'
                                            }}
                                        />
                                    </div>
                                </div>
                            </div>
                        )}
                            
                        
                        {/* Analysis window */}
                        {analysis2 && (
                            <div className="col-5 pt-2 image-analysis-form">
                                {/* Row for entropy */}
                                <div className="row">
                                    <div className="d-flex justify-content-center">
                                        <h5><strong>Entropy:</strong> {analysis2.entropy?.toFixed(4)}</h5>
                                    </div>
                                </div>
                                    
                                {/* Row for viewport */}
                                <div className="row">

                                </div>


                                {/* Row for byte graph */}
                                <div className="row">
                                    <div className="mt-3 p-3 bg-white border rounded shadow-sm">
                                        <ByteFrequencyChart byteCounts={analysis2.byte_counts} />
                                    </div>
                                </div>
                                

                            </div>
                        )}
                        
                        
                
                    <div className="col-6">


                    </div>

                </div>

                {/* Row containing Return and Submit buttons along with sizes and file type */}
                <div className="row py-4 justify-content-evenly">

                    {/* Return button */}
                    <div className="col-2 pt-3 d-grid">
                        <button 
                            type="button" 
                            className="btn btn-secondary"
                            style={{ height: '2.5vw' }}
                            onClick={ handleReturnClick }>
                            Return
                        </button>
                    </div>

                    {/* Submit button */}
                    <div className="col-2 pt-3 d-grid">
                        <button 
                            type="button" 
                            className="btn btn-success"
                            style={{ height: '2.5vw' }}
                            onClick={ handleReset }>
                            Reset
                        </button>
                    </div>

                </div>

                {/* Row for error message */}
                <div className="row text-center" style={{ color: 'red' }}>
                    <p>{ errorMessage }</p>
                </div>

            </div>    
        </>
    );
    
};

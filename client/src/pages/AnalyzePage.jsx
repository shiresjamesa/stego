import { useNavigate, useOutletContext } from 'react-router-dom';
import { useState } from 'react';
import axios from '../api/axios';
import ByteFrequencyChart from '../components/ByteFrequencyChart';
import RGBHistogramChart from '../components/RGBHistogramChart';


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

    const handleFileChange = async (e) => {
        const selectedFile = e.target.files[0];
        const inputId = e.target.id;
    
        if (!selectedFile) return;
    
        const fileType = selectedFile.type;
        if (fileType !== "image/png" && fileType !== "image/jpeg") return;
    
        const objectUrl = URL.createObjectURL(selectedFile);
    
        const isOriginal = inputId === "fileUpload1";
        if (isOriginal) {
            setFile1(selectedFile);
            setPreview1(objectUrl);
            await analyzeImage(selectedFile, setAnalysis1);
        } else {
            setFile2(selectedFile);
            setPreview2(objectUrl);
            await analyzeImage(selectedFile, setAnalysis2);
        }
    };
    

    const analyzeImage = async (file, setAnalysis) => {
        const formData = new FormData();
        formData.append('file', file);
    
        try {
            const response = await axios.post('/analyze/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
    
            console.log("Analysis Response:", response.data);
            setAnalysis(response.data);
    
        } catch (error) {
            console.error("Analysis failed:", error);
            setAnalysis({ error: "Failed to analyze image." });
        }
    };

    // Render RGB statistics
    const renderRgbStatsTable = (rgbStats) => {
        const stats = ['mean', 'median', 'mode', 'std_dev', 'skewness', 'kurtosis'];
    
        return (
            <table className="table table-bordered table-striped table-responsive">
                <thead>
                    <tr>
                        <th>Statistic</th>
                        <th>Red</th>
                        <th>Green</th>
                        <th>Blue</th>
                    </tr>
                </thead>
                <tbody>
                    {stats.map((stat) => (
                        <tr key={stat}>
                            <td>{stat.charAt(0).toUpperCase() + stat.slice(1)}</td>
                            <td>{rgbStats.R[stat].toFixed(4)}</td>
                            <td>{rgbStats.G[stat].toFixed(4)}</td>
                            <td>{rgbStats.B[stat].toFixed(4)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        );
    };

    // Render other byte statistics
    const renderOtherStats = (overallStats) => {
        return (
            <table className="table table-bordered table-striped table-responsive">
                <thead>
                    <tr>
                        <th>Statistic</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Entropy</td>
                        <td>{overallStats.entropy.toFixed(7)}</td>
                    </tr>
                    <tr>
                        <td>LSB Uniformity</td>
                        <td>{overallStats.lsb_uniformity.toFixed(7)}</td>
                    </tr>
                    <tr>
                        <td>Even Byte Ratio</td>
                        <td>{overallStats.even_ratio.toFixed(3)}</td>
                    </tr>
                    <tr>
                        <td>Odd Byte Ratio</td>
                        <td>{overallStats.odd_ratio.toFixed(3)}</td>
                    </tr>
                    <tr>
                        <td>Mean</td>
                        <td>{overallStats.mean.toFixed(7)}</td>
                    </tr>
                    <tr>
                        <td>Median</td>
                        <td>{overallStats.median}</td>
                    </tr>
                    <tr>
                        <td>Mode</td>
                        <td>{overallStats.mode}</td>
                    </tr>
                    <tr>
                        <td>Standard Deviation</td>
                        <td>{overallStats.std_dev.toFixed(7)}</td>
                    </tr>
                    <tr>
                        <td>Skewness</td>
                        <td>{overallStats.skewness.toFixed(7)}</td>
                    </tr>
                    <tr>
                        <td>Kurtosis</td>
                        <td>{overallStats.kurtosis.toFixed(7)}</td>
                    </tr>
                </tbody>
            </table>
        );
    };

    // Helper function to format the file size
    const formatFileSize = (size) => {
        if (size < 1024) return `${size} bytes`;
        if (size < 1024 * 1024) return `${(size / 1024).toFixed(2)} KB`;
        return `${(size / (1024 * 1024)).toFixed(2)} MB`;
    }

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

                    {/* File upload 1 window */}
                    {!analysis1 && (
                        <div className="col-5 pt-2 image-analysis-form" style={{ alignItems: 'center', justifyContent: 'center'}}>
                            <div className="row">

                                <div className="form-group text-center">
                                    <label htmlFor="fileUpload" className="form-label">Upload Original Media:</label>
                                    <input 
                                        type="file" 
                                        className="form-control" 
                                        id="fileUpload1" 
                                        onChange={ handleFileChange } 
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
                           
                    {/* Analysis 1 window */}
                    {analysis1 && (
                        <div className="col-5 pt-2">
                            <div className="image-analysis-form" style={{ overflowY: 'auto', overflowX: 'hidden', backgroundColor: '#fff' }}>
                                
                                {/* File metadata */}
                                <div className="row text-center mt-4">
                                    <div className="col-6">
                                        <h6><strong>File Name:</strong> {file1?.name}</h6>
                                    </div>
                                    <div className="col-6">
                                        <h6><strong>File Size:</strong> {formatFileSize(file1?.size)}</h6>
                                    </div>
                                </div>

                                {/* Overall byte statistics table */}
                                <div className="row mt-4 px-2">
                                    <h5>Overall Byte Statistics</h5>
                                </div>
                                <div className="row px-3">
                                    {renderOtherStats(analysis1.overall_byte_stats)}
                                </div>

                                {/* RGB channel statistics table */}
                                <div className="row mt-4 px-2">
                                    <h5>RGB Channel Statistics</h5>
                                </div>
                                <div className="row px-3">
                                    {renderRgbStatsTable(analysis1.rgb_stats)}
                                </div>

                                {/* Byte Frequency Section */}
                                <div className="row mt-4 px-3">
                                    <div className="p-3 bg-white border rounded shadow-sm">
                                        <ByteFrequencyChart byteCounts={analysis1.byte_counts} title="Byte Frequency" />
                                    </div>
                                </div>

                                {/* Histogram Section */}
                                <div className="row mt-4 px-3">
                                    {analysis1?.histograms && (
                                        <div className="p-2 bg-white border rounded shadow-sm">
                                            <RGBHistogramChart histograms={analysis1.histograms} title="RGB Histogram" />
                                        </div>
                                    )}
                                </div>

                                

                            </div>
                        </div>
                    )}
                
                    {/* Spacer */}
                    <div className="col-1" />

                    {/* File upload 2 window */}
                    {!analysis2 && (
                        <div className="col-5 pt-2 image-analysis-form" style={{ alignItems: 'center', justifyContent: 'center'}}>
                            <div className="row">

                                <div className="form-group text-center">
                                    <label htmlFor="fileUpload" className="form-label">Upload Encoded Media:</label>
                                    <input 
                                        type="file" 
                                        className="form-control" 
                                        id="fileUpload2" 
                                        onChange={handleFileChange} 
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
                             
                    {/* Analysis 2 window */}
                    {analysis2 && (
                        <div className="col-5 pt-2">
                            <div className="image-analysis-form" style={{ overflowY: 'auto', overflowX: 'hidden', backgroundColor: '#fff' }}>
                                
                                {/* File metadata */}
                                <div className="row text-center mt-4">
                                    <div className="col-6">
                                        <h6><strong>File Name:</strong> {file2?.name}</h6>
                                    </div>
                                    <div className="col-6">
                                        <h6><strong>File Size:</strong> {formatFileSize(file2?.size)}</h6>
                                    </div>
                                </div>

                                {/* Overall byte statistics table */}
                                <div className="row mt-4 px-2">
                                    <h5>Overall Byte Statistics</h5>
                                </div>
                                <div className="row px-3">
                                    {renderOtherStats(analysis2.overall_byte_stats)}
                                </div>

                                {/* RGB channel statistics table */}
                                <div className="row mt-4 px-2">
                                    <h5>RGB Channel Statistics</h5>
                                </div>
                                <div className="row px-3">
                                    {renderRgbStatsTable(analysis2.rgb_stats)}
                                </div>

                                {/* Byte Frequency Section */}
                                <div className="row mt-4 px-3">
                                    <div className="p-3 bg-white border rounded shadow-sm">
                                        <ByteFrequencyChart byteCounts={analysis2.byte_counts} title="Byte Frequency" />
                                    </div>
                                </div>

                                {/* Histogram Section */}
                                <div className="row mt-4 px-3">
                                    {analysis2?.histograms && (
                                        <div className="p-2 bg-white border rounded shadow-sm">
                                            <RGBHistogramChart histograms={analysis2.histograms} title="RGB Histogram" />
                                        </div>
                                    )}
                                </div>

                                

                            </div>
                        </div>
                    )}

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

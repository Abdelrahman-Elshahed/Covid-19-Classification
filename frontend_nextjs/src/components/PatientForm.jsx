// src/components/PatientForm.jsx
import { useState } from 'react';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import { format } from 'date-fns';

export default function PatientForm({ onSubmit, isLoading }) {
  // Form state matching Streamlit defaults
  const [patientData, setPatientData] = useState({
    Age: 70,
    Gender: "Male",
    Region: "Hovedstaden",
    Preexisting_Condition: "Diabetes",
    COVID_Strain: "Omicron",
    Symptoms: "Moderate",
    Severity: "Moderate",
    Hospitalized: "Yes",
    ICU_Admission: "No",
    Ventilator_Support: "No",
    Recovered: "Yes",
    Vaccination_Status: "Yes",
    Vaccine_Type: "Pfizer",
    Doses_Received: 2,
    Long_COVID_Symptoms: "Fatigue",
    Occupation: "Teacher",
    Smoking_Status: "Current",
    BMI: 35.0,
    Recovery_Classification: "Typical Recovery"
  });

  // Date states with Streamlit defaults
  const [dateOfInfection, setDateOfInfection] = useState(new Date('2023-04-15'));
  const [dateOfRecovery, setDateOfRecovery] = useState(new Date('2023-05-10'));
  const [dateOfReinfection, setDateOfReinfection] = useState(new Date('2024-05-10'));
  const [dateOfLastDose, setDateOfLastDose] = useState(new Date('2023-01-15'));
  const [hospitalAdmissionDate, setHospitalAdmissionDate] = useState(new Date('2023-04-18'));
  const [hospitalDischargeDate, setHospitalDischargeDate] = useState(new Date('2023-04-25'));

  const handleChange = (e) => {
    const { name, value } = e.target;
    setPatientData({
      ...patientData,
      [name]: value
    });
  };

  const handleNumberChange = (e) => {
    const { name, value } = e.target;
    setPatientData({
      ...patientData,
      [name]: parseFloat(value)
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Format dates for API
    const formatDate = (date) => format(date, "yyyy-MM-dd'T'00:00:00.000'Z'");
    
    const formattedData = {
      ...patientData,
      Date_of_Infection: formatDate(dateOfInfection),
      Date_of_Recovery: formatDate(dateOfRecovery),
      Date_of_Reinfection: formatDate(dateOfReinfection),
      Date_of_Last_Dose: formatDate(dateOfLastDose),
      Hospital_Admission_Date: formatDate(hospitalAdmissionDate),
      Hospital_Discharge_Date: formatDate(hospitalDischargeDate),
    };
    
    onSubmit(formattedData);
  };

  return (
    <div className="bg-white shadow-lg rounded-lg p-6">
      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Main title */}
        <div className="border-b pb-4">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Patient Information</h2>
          <p className="text-gray-600">Fill in the form below with the patient details to get a prediction.</p>
        </div>
        
        {/* Main Patient Information */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column */}
          <div className="space-y-6">
            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="text-lg font-semibold text-blue-900 mb-4">Basic Information</h3>
              
              {/* Age */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Age</label>
                <input
                  type="number"
                  name="Age"
                  value={patientData.Age}
                  onChange={handleNumberChange}
                  min="0"
                  max="120"
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              {/* Gender */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Gender</label>
                <select
                  name="Gender"
                  value={patientData.Gender}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                </select>
              </div>
              
              {/* Region */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Region</label>
                <select
                  name="Region"
                  value={patientData.Region}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Hovedstaden">Hovedstaden</option>
                  <option value="Sjælland">Sjælland</option>
                  <option value="Syddanmark">Syddanmark</option>
                  <option value="Midtjylland">Midtjylland</option>
                  <option value="Nordjylland">Nordjylland</option>
                </select>
              </div>
              
              {/* Preexisting Conditions */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Preexisting Condition</label>
                <select
                  name="Preexisting_Condition"
                  value={patientData.Preexisting_Condition}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Diabetes">Diabetes</option>
                  <option value="Asthma">Asthma</option>
                  <option value="Hypertension">Hypertension</option>
                  <option value="Obesity">Obesity</option>
                  <option value="Cardiovascular">Cardiovascular</option>
                </select>
              </div>
              
              {/* COVID Strain */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">COVID Strain</label>
                <select
                  name="COVID_Strain"
                  value={patientData.COVID_Strain}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Omicron">Omicron</option>
                  <option value="Beta">Beta</option>
                  <option value="Delta">Delta</option>
                  <option value="Alpha">Alpha</option>
                  <option value="XBB.1.5">XBB.1.5</option>
                </select>
              </div>
              
              {/* Symptoms */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Symptoms</label>
                <select
                  name="Symptoms"
                  value={patientData.Symptoms}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Moderate">Moderate</option>
                  <option value="Mild">Mild</option>
                  <option value="Severe">Severe</option>
                </select>
              </div>
              
              {/* Severity */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Severity</label>
                <select
                  name="Severity"
                  value={patientData.Severity}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Moderate">Moderate</option>
                  <option value="Low">Low</option>
                  <option value="High">High</option>
                  <option value="Critical">Critical</option>
                </select>
              </div>
              
              {/* Hospitalized */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Hospitalized</label>
                <select
                  name="Hospitalized"
                  value={patientData.Hospitalized}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>
              
              {/* Hospital dates - conditional */}
              {patientData.Hospitalized === "Yes" && (
                <div className="bg-yellow-50 p-3 rounded border-l-4 border-yellow-400 mb-4">
                  <div className="mb-3">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Hospital Admission Date</label>
                    <DatePicker
                      selected={hospitalAdmissionDate}
                      onChange={date => setHospitalAdmissionDate(date)}
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      dateFormat="yyyy-MM-dd"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Hospital Discharge Date</label>
                    <DatePicker
                      selected={hospitalDischargeDate}
                      onChange={date => setHospitalDischargeDate(date)}
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      dateFormat="yyyy-MM-dd"
                    />
                  </div>
                </div>
              )}
            </div>
          </div>
          
          {/* Right Column */}
          <div className="space-y-6">
            <div className="bg-green-50 p-4 rounded-lg">
              <h3 className="text-lg font-semibold text-green-900 mb-4">Medical Details</h3>
              
              {/* ICU Admission */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">ICU Admission</label>
                <select
                  name="ICU_Admission"
                  value={patientData.ICU_Admission}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="No">No</option>
                  <option value="Yes">Yes</option>
                </select>
              </div>
              
              {/* Ventilator Support */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Ventilator Support</label>
                <select
                  name="Ventilator_Support"
                  value={patientData.Ventilator_Support}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="No">No</option>
                  <option value="Yes">Yes</option>
                </select>
              </div>
              
              {/* Recovered */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Recovered</label>
                <select
                  name="Recovered"
                  value={patientData.Recovered}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>
              
              {/* Date of Infection */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Date of Infection</label>
                <DatePicker
                  selected={dateOfInfection}
                  onChange={date => setDateOfInfection(date)}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  dateFormat="yyyy-MM-dd"
                />
              </div>
              
              {/* Date of Recovery - conditional */}
              {patientData.Recovered === "Yes" && (
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Date of Recovery</label>
                  <DatePicker
                    selected={dateOfRecovery}
                    onChange={date => setDateOfRecovery(date)}
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    dateFormat="yyyy-MM-dd"
                  />
                </div>
              )}
              
              {/* Date of Reinfection */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Date of Reinfection (if applicable)</label>
                <DatePicker
                  selected={dateOfReinfection}
                  onChange={date => setDateOfReinfection(date)}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  dateFormat="yyyy-MM-dd"
                />
              </div>
              
              {/* Vaccination Status */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Vaccination Status</label>
                <select
                  name="Vaccination_Status"
                  value={patientData.Vaccination_Status}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>
              
              {/* Vaccine details - conditional */}
              {patientData.Vaccination_Status === "Yes" && (
                <div className="bg-purple-50 p-3 rounded border-l-4 border-purple-400 mb-4">
                  <div className="mb-3">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Vaccine Type</label>
                    <select
                      name="Vaccine_Type"
                      value={patientData.Vaccine_Type}
                      onChange={handleChange}
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="Pfizer">Pfizer</option>
                      <option value="Moderna">Moderna</option>
                      <option value="AstraZeneca">AstraZeneca</option>
                      <option value="Janssen">Janssen</option>
                    </select>
                  </div>
                  
                  <div className="mb-3">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Doses Received</label>
                    <input
                      type="number"
                      name="Doses_Received"
                      value={patientData.Doses_Received}
                      onChange={handleNumberChange}
                      min="0"
                      max="5"
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Date of Last Dose</label>
                    <DatePicker
                      selected={dateOfLastDose}
                      onChange={date => setDateOfLastDose(date)}
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      dateFormat="yyyy-MM-dd"
                    />
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
        
        {/* Additional Information Section */}
        <div className="border-t pt-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Additional Information</h2>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left Additional Column */}
            <div className="bg-orange-50 p-4 rounded-lg">
              <h3 className="text-lg font-semibold text-orange-900 mb-4">Lifestyle & Symptoms</h3>
              
              {/* Long COVID Symptoms */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Long COVID Symptoms</label>
                <select
                  name="Long_COVID_Symptoms"
                  value={patientData.Long_COVID_Symptoms}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Fatigue">Fatigue</option>
                  <option value="Brain Fog">Brain Fog</option>
                  <option value="Shortness of Breath">Shortness of Breath</option>
                  <option value="None">None</option>
                  <option value="Chest Pain">Chest Pain</option>
                </select>
              </div>
              
              {/* Occupation */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Occupation</label>
                <select
                  name="Occupation"
                  value={patientData.Occupation}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Teacher">Teacher</option>
                  <option value="Healthcare">Healthcare</option>
                  <option value="Office Worker">Office Worker</option>
                  <option value="Driver">Driver</option>
                  <option value="Student">Student</option>
                  <option value="Unemployed">Unemployed</option>
                </select>
              </div>
            </div>
            
            {/* Right Additional Column */}
            <div className="bg-red-50 p-4 rounded-lg">
              <h3 className="text-lg font-semibold text-red-900 mb-4">Health Metrics</h3>
              
              {/* Smoking Status */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Smoking Status</label>
                <select
                  name="Smoking_Status"
                  value={patientData.Smoking_Status}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Current">Current</option>
                  <option value="Never">Never</option>
                  <option value="Former">Former</option>
                </select>
              </div>
              
              {/* BMI */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">BMI</label>
                <input
                  type="number"
                  name="BMI"
                  value={patientData.BMI}
                  onChange={handleNumberChange}
                  min="10.0"
                  max="60.0"
                  step="0.1"
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              {/* Recovery Classification */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Recovery Classification</label>
                <select
                  name="Recovery_Classification"
                  value={patientData.Recovery_Classification}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Typical Recovery">Typical Recovery</option>
                  <option value="Fast Recovery">Fast Recovery</option>
                  <option value="Delayed Recovery">Delayed Recovery</option>
                </select>
              </div>
            </div>
          </div>
        </div>
        
        {/* Submit Button */}
        <div className="border-t pt-6 text-center">
          <button
            type="submit"
            disabled={isLoading}
            className={`px-8 py-3 rounded-lg font-semibold text-white transition-all duration-200 shadow-lg ${
              isLoading 
                ? 'bg-gray-400 cursor-not-allowed' 
                : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transform hover:scale-105'
            }`}
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing Prediction...
              </span>
            ) : (
              '🦠 Predict Reinfection Risk'
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
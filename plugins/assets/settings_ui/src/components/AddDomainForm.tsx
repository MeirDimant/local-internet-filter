import { useState } from "react";

interface AddDomainFormProps {
  onDomainAdded: () => void;
}

const AddDomainForm: React.FC<AddDomainFormProps> = ({ onDomainAdded }) => {
  // State variable to manage the new domain input value
  const [newDomain, setNewDomain] = useState<string>("");

  // Function to handle adding a new domain
  const handleAddDomain = async () => {
    try {
      const response = await fetch("http://settings.it/api/approved-domains", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ domain: newDomain }), // Send the new domain as the request body
      });
      if (response.ok) {
        setNewDomain(""); // Reset the input field
        onDomainAdded(); // Callback to indicate a domain was added
      }
    } catch (error) {
      console.error("Error adding domain:", error);
    }
  };

  return (
    <div className="add-section">
      {/* Input field for the new domain */}
      <input
        type="text"
        className="add-input"
        value={newDomain}
        onChange={(e) => setNewDomain(e.target.value)}
        placeholder="Add new domain"
      />
      {/* Button to add the new domain */}
      <button className="add-btn" onClick={handleAddDomain}>
        Add
      </button>
    </div>
  );
};

export default AddDomainForm;

import { useState, useEffect } from "react";

interface ApprovedDomainsListProps {
  refreshKey: number;
}

const ApprovedDomainsList: React.FC<ApprovedDomainsListProps> = ({
  refreshKey,
}) => {
  const [domains, setDomains] = useState<string[]>([]);

  const fetchDomains = async () => {
    try {
      const response = await fetch("http://settings.it/api/approved-domains");
      const data: string[] = await response.json();
      setDomains(data);
    } catch (error) {
      console.error("Error fetching approved domains:", error);
    }
  };

  useEffect(() => {
    fetchDomains();
  }, [refreshKey]);

  const handleDelete = (domain: string) => {
    fetch("http://settings.it/api/approved-domains", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ domain }),
    })
      .then((response) => response.json())
      .then((data) => setDomains(data));
  };

  return (
    <div>
      <h1>Approved Domains</h1>
      <ul className="list">
        {domains.map((domain) => (
          <li key={domain} className="list-item">
            {domain}
            <button className="delete-btn" onClick={() => handleDelete(domain)}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ApprovedDomainsList;

import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { format, parseISO } from 'date-fns';
import styles from '../styles/CDRTable.module.css';

interface CDR {
  id: string;
  source: string;
  destination: string;
  serviceType: string;
  startTime: string;
  usage: number;
  cost?: number;
  status?: string;
}

const CDRTable: React.FC = () => {
  const [cdrs, setCdrs] = useState<CDR[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sortField, setSortField] = useState<keyof CDR>('startTime');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchCdrs = async () => {
      try {
        setIsLoading(true);
        const response = await api.get('/cdrs');

        const transformedData = response.data.map((item: any) => ({
          id: item.id || String(Math.random()),
          source: item.source,
          destination: item.destination,
          serviceType: item.serviceType,
          startTime: item.startTime || item.startedAt || item.start_time,
          usage: Number(item.usage || item.duration),
          cost: item.cost,
          status: item.status,
        }));

        setCdrs(transformedData);
      } catch (err) {
        console.error('Failed to fetch CDRs:', err);
        setError('Failed to load CDR records. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchCdrs();
  }, []);

  const formatDateTime = (dateString: string) => {
    try {
      return format(parseISO(dateString), 'PPpp');
    } catch {
      return dateString;
    }
  };

  const formatUsage = (usage: number, serviceType: string): string => {
    switch (serviceType.toUpperCase()) {
      case 'VOICE':
        return `${usage.toFixed(2)} minutes`;
      case 'SMS':
        return `${Math.round(usage)} messages`;
      case 'DATA':
        return `${usage.toFixed(2)} MB`;
      default:
        return `${usage} units`;
    }
  };

  const sortedAndFilteredCdrs = React.useMemo(() => {
    return [...cdrs]
      .filter((cdr) => {
        if (!searchTerm) return true;
        const term = searchTerm.toLowerCase();
        return (
          cdr.source.toLowerCase().includes(term) ||
          cdr.destination.toLowerCase().includes(term) ||
          cdr.serviceType.toLowerCase().includes(term) ||
          cdr.startTime.toLowerCase().includes(term) ||
          String(cdr.usage).includes(term) ||
          (cdr.cost !== undefined && String(cdr.cost).includes(term)) ||
          (cdr.status && cdr.status.toLowerCase().includes(term))
        );
      })
      .sort((a, b) => {
        if (sortField === 'startTime') {
          const dateA = new Date(a[sortField]).getTime();
          const dateB = new Date(b[sortField]).getTime();
          return sortDirection === 'asc' ? dateA - dateB : dateB - dateA;
        }

        if (sortField === 'usage') {
          return sortDirection === 'asc' ? a.usage - b.usage : b.usage - a.usage;
        }

        const valA = String(a[sortField]).toLowerCase();
        const valB = String(b[sortField]).toLowerCase();
        return sortDirection === 'asc' ? valA.localeCompare(valB) : valB.localeCompare(valA);
      });
  }, [cdrs, sortField, sortDirection, searchTerm]);

  const handleSort = (field: keyof CDR) => {
    if (field === sortField) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  if (isLoading) {
    return (
      <div className={styles.loaderContainer}>
        <div className={styles.loader}></div>
        <span className={styles.loaderText}>Loading records...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.errorContainer}>
        <h3 className={styles.errorTitle}>Error Loading Data</h3>
        <p className={styles.errorText}>{error}</p>
        <button className={styles.retryButton} onClick={() => window.location.reload()}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2 className={styles.headerTitle}>Call Detail Records</h2>
        <p className={styles.headerSubtitle}>Comprehensive view of all communication activity</p>
      </div>

      <div className={styles.searchSection}>
        <div className={styles.searchContainer}>
          <div className={styles.searchInputWrapper}>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search records..."
              className={styles.searchInput}
            />
          </div>
        </div>
      </div>

      <div className={styles.tableContent}>
        <table className={styles.table}>
          <thead className={styles.tableHeader}>
            <tr>
              <th className={styles.tableHeaderCell} onClick={() => handleSort('source')}>
                Source
              </th>
              <th className={styles.tableHeaderCell} onClick={() => handleSort('destination')}>
                Destination
              </th>
              <th className={styles.tableHeaderCell} onClick={() => handleSort('serviceType')}>
                Service Type
              </th>
              <th className={styles.tableHeaderCell} onClick={() => handleSort('startTime')}>
                Start Time
              </th>
              <th className={styles.tableHeaderCell} onClick={() => handleSort('usage')}>
                Usage
              </th>
              {cdrs.some((cdr) => cdr.cost !== undefined) && (
                <th className={styles.tableHeaderCell}>Cost</th>
              )}
            </tr>
          </thead>
          <tbody>
            {sortedAndFilteredCdrs.length > 0 ? (
              sortedAndFilteredCdrs.map((cdr) => (
                <tr key={cdr.id} className={styles.tableRow}>
                  <td className={styles.tableCell}>{cdr.source}</td>
                  <td className={styles.tableCell}>{cdr.destination}</td>
                  <td className={styles.tableCell}>
                    <span
                      className={`${styles.badge} ${
                        cdr.serviceType === 'VOICE'
                          ? styles.voiceBadge
                          : cdr.serviceType === 'SMS'
                          ? styles.smsBadge
                          : cdr.serviceType === 'DATA'
                          ? styles.dataBadge
                          : styles.defaultBadge
                      }`}
                    >
                      {cdr.serviceType}
                    </span>
                  </td>
                  <td className={styles.tableCell}>{formatDateTime(cdr.startTime)}</td>
                  <td className={styles.tableCell}>{formatUsage(cdr.usage, cdr.serviceType)}</td>
                  {cdr.cost !== undefined && (
                    <td className={`${styles.tableCell} ${styles.costCell}`}>
                      ${cdr.cost.toFixed(2)}
                    </td>
                  )}
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={6} className={styles.noData}>
                  No records found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CDRTable;
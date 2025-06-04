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
  const [hoveredRow, setHoveredRow] = useState<string | null>(null);

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
          status: item.status
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

  const formatDuration = (seconds: number) => {
    if (seconds < 60) return `${seconds} sec`;
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds}s`;
  };

  const sortedAndFilteredCdrs = React.useMemo(() => {
    return [...cdrs]
      .filter(cdr => {
        if (!searchTerm) return true;
        const term = searchTerm.toLowerCase();
        return (
          cdr.source.toLowerCase().includes(term) ||
          cdr.destination.toLowerCase().includes(term) ||
          cdr.serviceType.toLowerCase().includes(term)||
          cdr.startTime.toLowerCase().includes(term) ||
          String(cdr.usage).includes(term) ||
          (cdr.cost !== undefined && String(cdr.cost).includes(term)) ||
          (cdr.status && cdr.status.toLowerCase().includes(term))
          || (cdr.id && cdr.id.toLowerCase().includes(term))||
          (cdr.startTime && cdr.startTime.toLowerCase().includes(term))||
          (cdr.source && cdr.source.toLowerCase().includes(term))
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
        <div className={styles.flexContainer}>
          <div>
            <svg 
              className={styles.errorIcon} 
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className={styles.marginLeft}>
            <h3 className={styles.errorTitle}>Error Loading Data</h3>
            <p className={styles.errorText}>{error}</p>
            <button 
              className={styles.retryButton}
              onClick={() => window.location.reload()}
            >
              Retry
            </button>
          </div>
        </div>
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
            <svg 
              className={styles.searchIcon}
              width="20" 
              height="20" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor"
              strokeWidth="2" 
              strokeLinecap="round" 
              strokeLinejoin="round"
            >
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
          </div>
          
          <div>
            <span className={styles.recordCount}>Total Records: </span>
            <span className={styles.recordCountValue}>{cdrs.length}</span>
          </div>
        </div>
      </div>
      
      <div className={styles.tableContent}>
        <table className={styles.table}>
          <thead className={styles.tableHeader}>
            <tr>
              <th 
                className={styles.tableHeaderCell}
                onClick={() => handleSort('source')}
              >
                <div className={styles.flexContainer + ' ' + styles.alignCenter}>
                  Source
                  {sortField === 'source' && (
                    <svg 
                      className={styles.sortIcon}
                      viewBox="0 0 24 24" 
                      fill="none" 
                      stroke="currentColor"
                      strokeWidth="2" 
                      strokeLinecap="round" 
                      strokeLinejoin="round"
                    >
                      <path d={sortDirection === 'asc' ? "M5 15l7-7 7 7" : "M19 9l-7 7-7-7"} />
                    </svg>
                  )}
                </div>
              </th>
              <th 
                className={styles.tableHeaderCell}
                onClick={() => handleSort('destination')}
              >
                <div className={styles.flexContainer + ' ' + styles.alignCenter}>
                  Destination
                  {sortField === 'destination' && (
                    <svg 
                      className={styles.sortIcon}
                      viewBox="0 0 24 24" 
                      fill="none" 
                      stroke="currentColor"
                      strokeWidth="2" 
                      strokeLinecap="round" 
                      strokeLinejoin="round"
                    >
                      <path d={sortDirection === 'asc' ? "M5 15l7-7 7 7" : "M19 9l-7 7-7-7"} />
                    </svg>
                  )}
                </div>
              </th>
              <th 
                className={styles.tableHeaderCell}
                onClick={() => handleSort('serviceType')}
              >
                <div className={styles.flexContainer + ' ' + styles.alignCenter}>
                  Service Type
                  {sortField === 'serviceType' && (
                    <svg 
                      className={styles.sortIcon}
                      viewBox="0 0 24 24" 
                      fill="none" 
                      stroke="currentColor"
                      strokeWidth="2" 
                      strokeLinecap="round" 
                      strokeLinejoin="round"
                    >
                      <path d={sortDirection === 'asc' ? "M5 15l7-7 7 7" : "M19 9l-7 7-7-7"} />
                    </svg>
                  )}
                </div>
              </th>
              <th 
                className={styles.tableHeaderCell}
                onClick={() => handleSort('startTime')}
              >
                <div className={styles.flexContainer + ' ' + styles.alignCenter}>
                  Start Time
                  {sortField === 'startTime' && (
                    <svg 
                      className={styles.sortIcon}
                      viewBox="0 0 24 24" 
                      fill="none" 
                      stroke="currentColor"
                      strokeWidth="2" 
                      strokeLinecap="round" 
                      strokeLinejoin="round"
                    >
                      <path d={sortDirection === 'asc' ? "M5 15l7-7 7 7" : "M19 9l-7 7-7-7"} />
                    </svg>
                  )}
                </div>
              </th>
              <th 
                className={styles.tableHeaderCell}
                onClick={() => handleSort('usage')}
              >
                <div className={styles.flexContainer + ' ' + styles.alignCenter}>
                  Duration
                  {sortField === 'usage' && (
                    <svg 
                      className={styles.sortIcon}
                      viewBox="0 0 24 24" 
                      fill="none" 
                      stroke="currentColor"
                      strokeWidth="2" 
                      strokeLinecap="round" 
                      strokeLinejoin="round"
                    >
                      <path d={sortDirection === 'asc' ? "M5 15l7-7 7 7" : "M19 9l-7 7-7-7"} />
                    </svg>
                  )}
                </div>
              </th>
              {cdrs.some(cdr => cdr.cost !== undefined) && (
                <th className={styles.tableHeaderCell}>Cost</th>
              )}
            </tr>
          </thead>
          <tbody>
            {sortedAndFilteredCdrs.length > 0 ? (
              sortedAndFilteredCdrs.map((cdr) => (
                <tr 
                  key={cdr.id} 
                  className={`${styles.tableRow} ${hoveredRow === cdr.id ? styles.tableRowHover : ''}`}
                  onMouseEnter={() => setHoveredRow(cdr.id)}
                  onMouseLeave={() => setHoveredRow(null)}
                >
                  <td className={styles.tableCell}>{cdr.source}</td>
                  <td className={styles.tableCell}>{cdr.destination}</td>
                  <td className={styles.tableCell}>
                    <span className={`${styles.badge} ${
                      cdr.serviceType === 'VOICE' ? styles.voiceBadge : 
                      cdr.serviceType === 'SMS' ? styles.smsBadge : 
                      cdr.serviceType === 'DATA' ? styles.dataBadge :
                      styles.defaultBadge
                    }`}>
                      {cdr.serviceType}
                    </span>
                  </td>
                  <td className={styles.tableCell}>
                    <div className={styles.flexContainer + ' ' + styles.alignCenter}>
                      <svg 
                        className={styles.timeIcon}
                        width="16" 
                        height="16" 
                        viewBox="0 0 24 24" 
                        fill="none" 
                        stroke="currentColor"
                        strokeWidth="2" 
                        strokeLinecap="round" 
                        strokeLinejoin="round"
                      >
                        <circle cx="12" cy="12" r="10"></circle>
                        <polyline points="12 6 12 12 16 14"></polyline>
                      </svg>
                      {formatDateTime(cdr.startTime)}
                    </div>
                  </td>
                  <td className={styles.tableCell}>
                    <span className={`${styles.durationBadge} ${
                      cdr.usage > 300 ? styles.longDuration : 
                      cdr.usage > 60 ? styles.mediumDuration : 
                      styles.shortDuration
                    }`}>
                      {formatDuration(cdr.usage)}
                    </span>
                  </td>
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
                  <svg 
                    className={styles.noDataIcon}
                    viewBox="0 0 24 24" 
                    fill="none" 
                    stroke="currentColor"
                    strokeWidth="1" 
                    strokeLinecap="round" 
                    strokeLinejoin="round"
                  >
                    <circle cx="12" cy="12" r="10"></circle>
                    <path d="M8 14s1.5 2 4 2 4-2 4-2"></path>
                    <line x1="9" y1="9" x2="9.01" y2="9"></line>
                    <line x1="15" y1="9" x2="15.01" y2="9"></line>
                  </svg>
                  <p className={styles.noDataText}>
                    {searchTerm ? "No matching records found" : "No CDR records available"}
                  </p>
                  {searchTerm && (
                    <button
                      className={styles.clearSearchButton}
                      onClick={() => setSearchTerm('')}
                    >
                      Clear search
                    </button>
                  )}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      
      {sortedAndFilteredCdrs.length > 0 && (
        <div className={styles.footer}>
          <div>
            Showing {sortedAndFilteredCdrs.length} {sortedAndFilteredCdrs.length === 1 ? 'record' : 'records'}
            {searchTerm && <span> matching "<strong>{searchTerm}</strong>"</span>}
          </div>
          <button
            className={styles.exportButton}
            onClick={() => {
              const headers = ['Source', 'Destination', 'Service Type', 'Start Time', 'Duration', 'Cost'];
              const csvContent = [
                headers.join(','),
                ...sortedAndFilteredCdrs.map(cdr => [
                  cdr.source,
                  cdr.destination,
                  cdr.serviceType,
                  formatDateTime(cdr.startTime),
                  formatDuration(cdr.usage),
                  cdr.cost ? `$${cdr.cost.toFixed(2)}` : ''
                ].join(','))
              ].join('\n');
              
              const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
              const url = URL.createObjectURL(blob);
              const link = document.createElement('a');
              link.href = url;
              link.download = `cdr-export-${new Date().toISOString().slice(0,10)}.csv`;
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
            }}
          >
            <svg 
              width="20"
              height="20"
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor"
              strokeWidth="2" 
              strokeLinecap="round" 
              strokeLinejoin="round"
              className={styles.iconMarginRight}
            >
              <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"></path>
              <polyline points="7 10 12 15 17 10"></polyline>
              <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
            Export CSV
          </button>
        </div>
      )}
    </div>
  );
};

export default CDRTable;
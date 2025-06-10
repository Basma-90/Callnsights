import React, { useEffect, useMemo, useState } from 'react';
import api from '../services/api';
import { Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  type ChartOptions,
} from 'chart.js';
import styles from '../styles/Reports.module.css';

ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

type ReportType = 'day' | 'service' | 'source' | 'destination';

interface BaseData {
  totalUsage: number;
  callCount: number;
  usageUnit?: string; 
}

interface DailyUsageData extends BaseData {
  date: string;
}
interface ServiceTypeData extends BaseData {
  serviceType: string;
}
interface SourceData extends BaseData {
  source: string;
}
interface DestinationData extends BaseData {
  destination: string;
}

interface ChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    backgroundColor: string | string[];
    borderColor?: string | string[];
    borderWidth?: number;
  }[];
}


const formatUsage = (usage: number, usageUnit?: string): string => {
  if (!usageUnit) return `${usage} units`;
  return `${usage.toFixed(2)} ${usageUnit}`;
};

const ReportCharts: React.FC = () => {
  const [reportType, setReportType] = useState<ReportType>('day');
  const [data, setData] = useState<BaseData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [serviceTypeFilter, setServiceTypeFilter] = useState('');

  const fetchReportData = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams({ groupBy: reportType });
      if (startDate) params.append('startDate', startDate);
      if (endDate) params.append('endDate', endDate);
      if (serviceTypeFilter && reportType === 'day') {
        params.append('serviceType', serviceTypeFilter);
      }

      const response = await api.get(`cdrs/aggregated?${params.toString()}`);
      setData(response.data);
    } catch (err: any) {
      setError(err?.response?.data?.message || 'Failed to fetch data');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchReportData();
  }, [reportType]);

  const applyFilters = () => {
    if (startDate && endDate && new Date(startDate) > new Date(endDate)) {
      setError('Start date must be before end date');
      return;
    }
    fetchReportData();
  };

  const resetFilters = () => {
    setStartDate('');
    setEndDate('');
    setServiceTypeFilter('');
    fetchReportData();
  };

  const extractLabels = (item: any): string =>
    reportType === 'day' ? item.date :
    reportType === 'service' ? item.serviceType :
    reportType === 'source' ? item.source : item.destination;

  const chartData = useMemo<ChartData>(() => ({
    labels: data.map(extractLabels),
    datasets: reportType === 'day'
      ? [
          {
            label: `Usage (${data[0]?.usageUnit || 'units'})`, // Dynamically set the unit
            data: (data as DailyUsageData[]).map(d => d.totalUsage),
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
          },
          {
            label: 'Call Count',
            data: (data as DailyUsageData[]).map(d => d.callCount),
            backgroundColor: 'rgba(255, 159, 64, 0.6)',
            borderColor: 'rgba(255, 159, 64, 1)',
            borderWidth: 1,
          },
        ]
      : [
          {
            label: `Usage by ${reportType} (${data[0]?.usageUnit || 'units'})`, // Dynamically set the unit
            data: data.map(d => d.totalUsage),
            backgroundColor: reportType === 'service'
              ? ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
              : 'rgba(54, 162, 235, 0.6)',
            borderColor: reportType === 'service' ? '#fff' : 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
          },
        ],
  }), [data, reportType]);

  const chartOptions: ChartOptions<'bar' | 'pie'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: `Usage Report - ${reportType.toUpperCase()}` },
    },
    scales: reportType !== 'service' ? { y: { beginAtZero: true } } : {},
  };

  const renderChart = () => {
    if (reportType === 'service') return <Pie data={chartData} options={chartOptions as ChartOptions<'pie'>} />;
    return <Bar data={chartData} options={chartOptions as ChartOptions<'bar'>} />;
  };

  const totalUsage = useMemo(() => data.reduce((sum, d) => sum + d.totalUsage, 0), [data]);
  const totalCalls = useMemo(() => data.reduce((sum, d) => sum + d.callCount, 0), [data]);
  const avgCallDuration = useMemo(() =>
    totalCalls ? (totalUsage / totalCalls).toFixed(2) : '0', [totalUsage, totalCalls]);

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>CDR Report Dashboard</h2>

      <div className={styles.filters}>
        <select value={reportType} onChange={e => setReportType(e.target.value as ReportType)}>
          <option value="day">Daily</option>
          <option value="service">Service Type</option>
          <option value="source">Source</option>
          <option value="destination">Destination</option>
        </select>

        <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} />
        <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} />

        {reportType === 'day' && (
          <input
            type="text"
            placeholder="Service Type"
            value={serviceTypeFilter}
            onChange={e => setServiceTypeFilter(e.target.value)}
          />
        )}

        <button onClick={applyFilters} disabled={isLoading}>Apply</button>
        <button onClick={resetFilters} className={styles.reset} disabled={isLoading}>Reset</button>
      </div>

      {error && <div className={styles.error}>{error}</div>}

      {isLoading ? (
        <p className={styles.loading}>Loading...</p>
      ) : (
        <>
          <div className={styles.chartContainer}>{renderChart()}</div>
          <div className={styles.analysis}>
            <h3>Report Summary</h3>
            <ul>
              <li>
                <strong>Total Usage:</strong>{' '}
                {data.length > 0
                  ? formatUsage(totalUsage, data[0]?.usageUnit)
                  : 'No data available'}
              </li>
              <li>
                <strong>Total Calls:</strong>{' '}
                {data.length > 0 ? totalCalls : 'No data available'}
              </li>
              <li>
                <strong>Average Call Duration:</strong>{' '}
                {data.length > 0
                  ? formatUsage(Number(avgCallDuration), data[0]?.usageUnit) + '/call'
                  : 'No data available'}
              </li>
              <li>
                <strong>Report Type:</strong> {reportType}
              </li>
            </ul>
          </div>
        </>
      )}
    </div>
  );
};

export default ReportCharts;
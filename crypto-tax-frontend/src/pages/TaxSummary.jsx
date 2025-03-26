import React, { useState, useEffect } from "react";
import { Card, Table, Row, Col, message } from "antd";
import api from "../axios"; // ✅ Use configured axios
import moment from "moment";

const TaxSummary = () => {
  const [transactions, setTransactions] = useState([]);
  const [summary, setSummary] = useState({
    totalBuy: 0,
    totalSell: 0,
    profitLoss: 0,
    estimatedTax: 0,
  });

  // ✅ Get user_id from localStorage
  const userId = localStorage.getItem("user_id");

  // ✅ Fetch transaction data
  const fetchTransactions = async () => {
    try {
      const response = await api.get(`/transactions/show/${userId}`);
      if (response.data.length > 0) {
        setTransactions(response.data);
        calculateSummary(response.data); // ✅ Update tax summary
      } else {
        message.info("No transactions found.");
        setTransactions([]);
      }
    } catch (err) {
      console.error("❌ Error fetching transactions:", err);
      message.error("Error loading transactions.");
    }
  };

  // ✅ Calculate tax summary
  const calculateSummary = (data) => {
    const totalBuy = data
      .filter((tx) => tx.transaction_type === "Buy")
      .reduce((sum, tx) => sum + tx.price * tx.quantity, 0);
    const totalSell = data
      .filter((tx) => tx.transaction_type === "Sell")
      .reduce((sum, tx) => sum + tx.price * tx.quantity, 0);

    const profitLoss = totalSell - totalBuy;
    const estimatedTax = profitLoss > 0 ? (profitLoss * 0.15).toFixed(2) : 0;

    setSummary({
      totalBuy,
      totalSell,
      profitLoss,
      estimatedTax,
    });
  };

  // ✅ Fetch data on component load
  useEffect(() => {
    fetchTransactions();
  }, []);

  // ✅ Transaction table columns
  const columns = [
    { title: "Type", dataIndex: "transaction_type", key: "transaction_type" },
    { title: "Crypto", dataIndex: "crypto_name", key: "crypto_name" },
    { title: "Quantity", dataIndex: "quantity", key: "quantity" },
    { title: "Price", dataIndex: "price", key: "price" },
    {
      title: "Date",
      dataIndex: "transaction_date",
      key: "transaction_date",
      render: (text) => moment(text).format("YYYY-MM-DD HH:mm"),
    },
  ];

  return (
    <div>
      <h2>📊 Tax Summary Overview</h2>

      {/* ✅ Summary Cards */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card title="💸 Total Buy Value" bordered={false}>
            <h2>₹{summary.totalBuy.toFixed(2)}</h2>
          </Card>
        </Col>
        <Col span={6}>
          <Card title="📉 Total Sell Value" bordered={false}>
            <h2>₹{summary.totalSell.toFixed(2)}</h2>
          </Card>
        </Col>
        <Col span={6}>
          <Card
            title={
              summary.profitLoss >= 0 ? "📈 Profit" : "📉 Loss"
            }
            bordered={false}
          >
            <h2 style={{ color: summary.profitLoss >= 0 ? "green" : "red" }}>
              ₹{summary.profitLoss.toFixed(2)}
            </h2>
          </Card>
        </Col>
        <Col span={6}>
          <Card title="💰 Estimated Tax (15%)" bordered={false}>
            <h2>₹{summary.estimatedTax}</h2>
          </Card>
        </Col>
      </Row>

      {/* ✅ Recent Taxable Transactions */}
      <Card title="📄 Recent Taxable Transactions" bordered={false}>
        <Table
          columns={columns}
          dataSource={transactions.filter((tx) => tx.transaction_type === "Sell").slice(0, 5)}
          rowKey="id"
        />
      </Card>
    </div>
  );
};

export default TaxSummary;

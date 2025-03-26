import React, { useState, useEffect } from "react";
import api from "../axios"; // ✅ Use configured axios instance
import {
  Table,
  Button,
  Modal,
  Form,
  Input,
  Select,
  InputNumber,
  DatePicker,
  message,
} from "antd";
import moment from "moment";
import { useNavigate } from "react-router-dom";

const { Option } = Select;

const Transactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [editingTransaction, setEditingTransaction] = useState(null);
  const [form] = Form.useForm();
  const [showTransactions, setShowTransactions] = useState(false); // ✅ Control showing transactions
  const [error, setError] = useState(""); // ✅ Fix added
  const navigate = useNavigate();

  // ✅ Get user_id dynamically from localStorage
  const userId = localStorage.getItem("user_id");

  // ✅ Fetch transactions when "Show Transactions" is clicked
  const fetchTransactions = async () => {
    try {
      const response = await api.get(`/transactions/show/${userId}`);

      if (response.data.message) {
        setTransactions([]); // No transactions, set empty array
        setError(response.data.message); // ✅ Show message if no data
      } else {
        setTransactions(response.data);
        setError(""); // ✅ Clear error if data exists
      }
      setShowTransactions(true); // ✅ Show transactions on success
    } catch (err) {
      setError("Error fetching transactions."); // ✅ Error on API failure
    }
  };

  // ✅ Show modal for add/edit
  const showModal = (transaction = null) => {
    setEditingTransaction(transaction);
    setIsModalVisible(true);

    if (transaction) {
      form.setFieldsValue({
        ...transaction,
        transaction_date: moment(transaction.transaction_date),
      });
    } else {
      form.resetFields();
    }
  };

  // ✅ Add or update transaction
  const handleOk = async () => {
    try {
      const values = await form.validateFields();
      values.transaction_date = values.transaction_date.format(
        "YYYY-MM-DDTHH:mm:ss"
      );

      if (editingTransaction) {
        // Update transaction
        await api.put(
          `/transactions/update/${editingTransaction.id}`,
          values
        );
        message.success("✅ Transaction updated successfully.");
      } else {
        // Add transaction
        await api.post("/transactions/create-transaction", {
          ...values,
          user_id: userId,
        });
        message.success("✅ Transaction added successfully.");
      }

      fetchTransactions(); // ✅ Refresh transactions after add/update
      setIsModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error("❌ Error adding/updating transaction:", error);
      message.error("❌ Error processing transaction.");
    }
  };

  // ✅ Delete transaction
  const handleDelete = async (userId, transactionId) => {
    try {
      const response = await api.delete(
        `/transactions/delete/${userId}/${transactionId}`
      );
      message.success(response.data.message);
      fetchTransactions(); // ✅ Refresh transactions after delete
    } catch (err) {
      console.error("❌ Error deleting transaction:", err);
      setError("Error deleting transaction.");
    }
  };
  

  // ✅ Table columns
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
    {
      title: "Actions",
      key: "actions",
      render: (_, record) => (
        <>
          <Button onClick={() => showModal(record)} style={{ marginRight: 8 }}>
            ✏️ Edit
          </Button>
          <Button danger onClick={() => handleDelete(userId, record.id)}>
  🗑️ Delete
</Button>

        </>
      ),
    },
  ];

  return (
    <div>
      <h2>📊 Transactions Management</h2>

      <div style={{ marginBottom: 16 }}>
        {/* ✅ Show Transactions Button */}
        <Button type="primary" onClick={fetchTransactions} style={{ marginRight: 8 }}>
          📄 Show Transactions
        </Button>

        {/* ✅ Add Transaction Button */}
        <Button type="default" onClick={() => showModal()}>
          ➕ Add Transaction
        </Button>
      </div>

      {/* ✅ Show error message if any */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* ✅ Show transactions if loaded */}
      {showTransactions ? (
        <Table
          columns={columns}
          dataSource={transactions}
          rowKey="id"
          style={{ marginTop: 20 }}
        />
      ) : (
        <p>Click "Show Transactions" to view your transaction history.</p>
      )}

      {/* ✅ Modal for add/edit */}
      <Modal
        title={editingTransaction ? "Edit Transaction" : "Add Transaction"}
        open={isModalVisible}
        onOk={handleOk}
        onCancel={() => setIsModalVisible(false)}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="transaction_type"
            label="Transaction Type"
            rules={[{ required: true, message: "Please select a type" }]}
          >
            <Select>
              <Option value="Buy">Buy</Option>
              <Option value="Sell">Sell</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="crypto_name"
            label="Crypto Name"
            rules={[{ required: true, message: "Enter crypto name" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="quantity"
            label="Quantity"
            rules={[{ required: true, message: "Enter quantity" }]}
          >
            <InputNumber style={{ width: "100%" }} />
          </Form.Item>
          <Form.Item
            name="price"
            label="Price"
            rules={[{ required: true, message: "Enter price" }]}
          >
            <InputNumber style={{ width: "100%" }} />
          </Form.Item>
          <Form.Item
            name="transaction_date"
            label="Transaction Date"
            rules={[{ required: true, message: "Select date" }]}
          >
            <DatePicker showTime style={{ width: "100%" }} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Transactions;

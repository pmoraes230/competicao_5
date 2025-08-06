function exportTicketToPDF(ticketId, clientName, sectorName, eventName, eventDate, issueDate, status, validationCode) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.setFont("helvetica", "normal");
    doc.setFontSize(16);
    doc.text("Ingresso para evento", 20, 20)

    doc.setFontSize(12);
    doc.setTextColor(0, 0, 0);
    doc.text(`Nome do cliente: ${clientName}`, 20, 40);
    doc.text(`Setor comprado: ${sectorName}`, 20, 50);
    doc.text(`Evento comprado: ${eventName}`, 20, 60);
    doc.text(`Data do evento: ${eventDate}`, 20, 70);
    doc.text(`Data de compra: ${issueDate}`, 20, 80);
    doc.text(`Status do ingresso: ${status}`, 20, 90);
    doc.text(`Código de validação: ${validationCode}`, 20, 100);

    doc.setLineWidth(0.5);

    doc.save(`ingresso_${ticketId}.pdf`)
}

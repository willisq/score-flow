import { jsPDF } from "jspdf";
import html2canvas from "html2canvas";

export function useBracketExport() {
  const exportToPdf = async (elementId: string, category: any) => {
    const element = document.getElementById(elementId);
    if (!element) {
      console.error("Element not found:", elementId);
      return;
    }

    try {
      // Create a temporary container to style for printing
      const originalStyle = element.getAttribute("style");
      
      // We want to capture it as it is, but maybe force high quality
      const canvas = await html2canvas(element, {
        scale: 2,
        useCORS: true,
        backgroundColor: "#ffffff", // Force white background for print
        logging: false,
      });

      const imgData = canvas.toDataURL("image/png");
      const pdf = new jsPDF({
        orientation: "landscape",
        unit: "mm",
        format: "a4",
      });

      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();
      
      // Header Information
      pdf.setFontSize(18);
      pdf.setTextColor(40);
      pdf.text(category.modalityName || "Pirámide de Competencia", 15, 20);
      
      pdf.setFontSize(10);
      pdf.setTextColor(100);
      const details = `${category.ageStr} | ${category.sexesStr} | ${category.ranksStr}${category.weightStr ? " | " + category.weightStr : ""}`;
      pdf.text(details, 15, 28);
      
      pdf.setDrawColor(200);
      pdf.line(15, 32, pageWidth - 15, 32);

      // Image metrics
      const imgProps = pdf.getImageProperties(imgData);
      const margin = 15;
      const contentWidth = pageWidth - 2 * margin;
      const contentHeight = (imgProps.height * contentWidth) / imgProps.width;

      // If content is too tall, scale down
      let finalHeight = contentHeight;
      let finalWidth = contentWidth;
      const maxAvailableHeight = pageHeight - 45; // Below header

      if (finalHeight > maxAvailableHeight) {
        finalHeight = maxAvailableHeight;
        finalWidth = (imgProps.width * finalHeight) / imgProps.height;
      }

      const xCentering = (pageWidth - finalWidth) / 2;
      pdf.addImage(imgData, "PNG", xCentering, 40, finalWidth, finalHeight);

      // Filename: Piramide_Modalidad_Rango.pdf
      const fileName = `Piramide_${category.modalityName.replace(/\s+/g, "_")}_${category.ranksStr.replace(/\s+/g, "_")}.pdf`;
      pdf.save(fileName);
      
    } catch (error) {
      console.error("Error generating PDF:", error);
    }
  };

  return {
    exportToPdf,
  };
}

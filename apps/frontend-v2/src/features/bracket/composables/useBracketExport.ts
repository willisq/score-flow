import { jsPDF } from "jspdf";
import html2canvas from "html2canvas";

export function useBracketExport() {
  const captureElement = async (elementId: string) => {
    const element = document.getElementById(elementId);
    if (!element) {
      console.error("Element not found:", elementId);
      return null;
    }

    const canvas = await html2canvas(element, {
      scale: 1.5,
      useCORS: true,
      backgroundColor: "#ffffff",
      logging: false,
    });
    return canvas.toDataURL("image/jpeg", 0.7);
  };

  const addBracketToPdf = (pdf: jsPDF, imgData: string, category: any) => {
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

    let finalHeight = contentHeight;
    let finalWidth = contentWidth;
    const maxAvailableHeight = pageHeight - 45;

    if (finalHeight > maxAvailableHeight) {
      finalHeight = maxAvailableHeight;
      finalWidth = (imgProps.width * finalHeight) / imgProps.height;
    }

    const xCentering = (pageWidth - finalWidth) / 2;
    pdf.addImage(imgData, "JPEG", xCentering, 40, finalWidth, finalHeight, undefined, "FAST");
  };

  const exportToPdf = async (elementId: string, category: any) => {
    try {
      const imgData = await captureElement(elementId);
      if (!imgData) return;

      const pdf = new jsPDF({
        orientation: category.orientation || "landscape",
        unit: "mm",
        format: "a4",
      });

      addBracketToPdf(pdf, imgData, category);

      const fileName = `Piramide_${category.modalityName.replace(/\s+/g, "_")}_${category.ranksStr.replace(/\s+/g, "_")}.pdf`;
      pdf.save(fileName);
    } catch (error) {
      console.error("Error generating PDF:", error);
    }
  };

  const exportAllToPdf = async (groups: any[]) => {
    try {
      if (groups.length === 0) return;

      // Create PDF with the first group's orientation
      const pdf = new jsPDF({
        orientation: groups[0].orientation || "landscape",
        unit: "mm",
        format: "a4",
      });

      for (let i = 0; i < groups.length; i++) {
        const group = groups[i];
        
        // Skip groups without an element ID (though they should have one)
        if (!group.elementId) continue;

        const imgData = await captureElement(group.elementId);
        if (!imgData) continue;

        if (i > 0) {
          pdf.addPage("a4", group.orientation || "landscape");
        }

        addBracketToPdf(pdf, imgData, group);
      }

      pdf.save("Reporte_Global_Piramides.pdf");
    } catch (error) {
      console.error("Error generating Global PDF:", error);
    }
  };

  return {
    exportToPdf,
    exportAllToPdf,
  };
}

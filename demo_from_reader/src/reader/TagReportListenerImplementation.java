package reader;

import java.util.List;
import java.io.FileWriter;
import com.impinj.octane.ImpinjReader;
import com.impinj.octane.Tag;
import com.impinj.octane.TagReport;
import com.impinj.octane.TagReportListener;

public class TagReportListenerImplementation implements TagReportListener{

	private FileWriter writer;
	private double txPower;
	private double RSSITotal;
	private int RSSICount;

	public TagReportListenerImplementation(String fileName){
		String filePath="./data/"+fileName+".txt";
		RSSITotal=0;
		RSSICount=0;
		try {
			writer =new FileWriter(filePath);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	@Override
	public void onTagReported(ImpinjReader arg0, TagReport report) {
		List<Tag> taglist=report.getTags();
		for(Tag tag:taglist) {
			System.out.print(" "+tag.getPeakRssiInDbm());
			RSSICount++;
			RSSITotal+=tag.getPeakRssiInDbm();
			
		}
		
	}
	
	public void setTxPower(double Dbm){
		
		try {
			if(RSSICount==0){
				writer.write("NAN"+" ");
				writer.flush();
			}
			else{
				writer.write(""+RSSITotal/RSSICount+" ");
				writer.flush();
			}
			
		} catch (Exception e) {
			e.printStackTrace();
		}
		RSSICount=0;
		RSSITotal=0;
		txPower=Dbm;
	}
	
}

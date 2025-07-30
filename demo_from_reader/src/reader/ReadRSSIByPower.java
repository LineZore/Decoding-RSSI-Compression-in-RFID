package reader;

import com.impinj.octane.*;
import java.util.*;

import reader.TagReportListenerImplementation;

public class ReadRSSIByPower {
    public static void main(String[] args) {
        try {
            ImpinjReader reader=new ImpinjReader();
            String hostName=args[0];
            reader.connect(hostName);

            Settings setting=reader.queryDefaultSettings();
            setting.setSearchMode(SearchMode.DualTarget);
            setting.setSession(1);

            AntennaConfigGroup antennas=setting.getAntennas();
            antennas.disableAll();
            antennas.enableById(new short[]{1});
            antennas.getAntenna((short) 1).setIsMaxRxSensitivity(true);
            antennas.getAntenna((short) 1).setTxPowerinDbm(10);

            Double fre[]={920.625};
            setting.setTxFrequenciesInMhz(new ArrayList<>(Arrays.asList(fre)) );

            //0 is FM0
            setting.setRfMode(0);

            FilterSettings fs= setting.getFilters();
            TagFilter tf= fs.getTagFilter1();
            tf.setMemoryBank(MemoryBank.Epc);
            tf.setBitPointer(BitPointers.Epc);
            tf.setBitCount(96);
            tf.setTagMask(args[1]);
            tf.setFilterOp(TagFilterOp.Match);

            fs.setMode(TagFilterMode.OnlyFilter1);
            fs.setTagFilter1(tf);
            setting.setFilters(fs);

            ReportConfig report= setting.getReport();
            report.setIncludePhaseAngle(true);
            report.setIncludePeakRssi(true);
            setting.setReport(report);

            TagReportListenerImplementation trl=new reader.TagReportListenerImplementation(args[2]);
            reader.setTagReportListener(trl);

            FeatureSet features=reader.queryFeatureSet();
            List<TxPowerTableEntry> newTxP= features.getTxPowers();
            for(TxPowerTableEntry t:newTxP){
                    System.out.println();
                    System.out.print(t.Dbm);
                    antennas.getAntenna((short) 1).setIsMaxTxPower(false);
                    antennas.getAntenna((short) 1).setTxPowerinDbm(t.Dbm);

                    reader.applySettings(setting);
                    reader.start();
                    try {
                        Thread.sleep(300);
                    } catch (InterruptedException e) {
                        throw new RuntimeException(e);
                    }
                    reader.stop();
                    trl.setTxPower(t.Dbm);
            }
            reader.disconnect();
        } catch (OctaneSdkException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
}

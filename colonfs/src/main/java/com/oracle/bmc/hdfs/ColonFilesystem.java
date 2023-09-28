package com.oracle.bmc.hdfs;

import java.io.IOException;
import java.util.List;

import com.google.common.collect.Lists;
import com.oracle.bmc.hdfs.BmcFilesystem;

import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.fs.PathFilter;

public class ColonFilesystem extends BmcFilesystem {
/*
  @Override
  public FileStatus[] globStatus(final Path pathPattern, final PathFilter filter)
      throws IOException {
    final FileStatus[] statusList = super.listStatus(pathPattern);
    final List<FileStatus> result = Lists.newLinkedList();
    for (FileStatus fileStatus : statusList) {
      if (filter.accept(fileStatus.getPath())) {
        result.add(fileStatus);
      }
    }
    return result.toArray(new FileStatus[] {});
  }
*/

  private static final PathFilter OCI_DEFAULT_FILTER = new PathFilter() {
      @Override
      public boolean accept(Path file) {
        return true;
      }
    };

  public FileStatus[] globStatus(Path pathPattern) throws IOException {
    return new OciGlobber(this, pathPattern, OCI_DEFAULT_FILTER).glob();
  }

  public FileStatus[] globStatus(Path pathPattern, PathFilter filter)
      throws IOException {
    return new OciGlobber(this, pathPattern, filter).glob();
  }

}

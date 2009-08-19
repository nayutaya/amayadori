#! ruby -Ku

def get_line_count(path)
  return File.readlines(path).size
end

test_files     = []
tested_files   = []
untested_files = []

Dir.glob("*.py").sort.each { |path|
  if /_test\.py$/i =~ path
    test_files << path
  elsif File.exist?(path.sub(/\.py/i, "_test.py"))
    tested_files << path
  else
    untested_files << path
  end
}

[test_files, tested_files, untested_files].each { |files|
  files.collect! { |path|
    [path, get_line_count(path)]
  }
}

puts("Test files:")
test_files.each { |path, count|
  printf("  %5i %s\n", count, path)
}
printf("  %5i\n", test_files.inject(0) { |sum, (path, count)| sum + count })

puts
puts("Tested files:")
tested_files.each { |path, count|
  printf("  %5i %s\n", count, path)
}
printf("  %5i\n", tested_files.inject(0) { |sum, (path, count)| sum + count })

puts
puts("Untested files:")
untested_files.each { |path, count|
  printf("  %5i %s\n", count, path)
}
printf("  %5i\n", untested_files.inject(0) { |sum, (path, count)| sum + count })

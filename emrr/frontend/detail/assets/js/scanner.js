function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#blah')
                .attr('src', e.target.result)
                .width(405)
                .height(586)
                .show(); // Make sure the image is displayed
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function showFinalImage() {
    $('#loading').show();
    $('#finalImageDiv').hide();
    
    // Generate a random delay between 3 to 9 seconds
    var randomDelay = Math.floor(Math.random() * (9000 - 3000 + 1)) + 3000;
    
    setTimeout(function() {
        var img = new Image();
        img.src = "/records/region_of_interests/form2_final.png";
        img.onload = function () {
            $('#loading').hide();
            $('#finalImageDiv').show();
            
            // Insert values into textboxes
            var values = {
                nama_pasien: "M. Aulia Hibatillah",
                nama_periusahaan: "-",
                ttl_umur: "30-07-2002/21",
                nama_peserta: "-",
                no_rm: "1165210073",
                no_polis: "-",
                tanggal_masuk: "04-05-2023",
                unit_rawat_terakhir: "Jiwa",
                riwayat_penyakit: "Asthma",
                pemeriksaan_fisik: "Tekanan Darah, -",
                pemeriksaan_penunjang: "-",
                pengobatan: "Sertalline 100mg",
                diagnosis_awal: "Depressive Episode",
                kode_icd_10: "F 32",
                diagnosis_utama: "PTSD",
                kode_icd_10_2: "F 17",
                diagnosis_lain: "-",
                tindakan: "Psikoterapi, Wawancara",
                kode_icd_9_cm: "13 IU",
                alergi: "-",
                keadaan_pulang: "-",
                anjuran: "-",
                tanggal_ttd: "Surabaya, 12 September 2023",
                dokter_penanggungjawab: "dr. Izzatul Fithriyah., Sp.KJ (K)"
            };
            
            for (var id in values) {
                $('input[name="' + id + '"]').val(values[id]);
            }
        };
    }, randomDelay);
}